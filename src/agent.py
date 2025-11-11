from __future__ import annotations

# Load environment variables FIRST, before any other imports
# This ensures LIVEKIT_API_KEY and other env vars are available when Worker initializes
from dotenv import load_dotenv
import os
import sys
from pathlib import Path

# Find the project root (parent of src directory)
project_root = Path(__file__).parent.parent
env_path = project_root / ".env"

# Load .env file and verify it exists
if env_path.exists():
    load_dotenv(dotenv_path=env_path, override=True)
else:
    print(f"Warning: .env file not found at {env_path}", file=sys.stderr)

# Verify required environment variables are set
if not os.getenv("LIVEKIT_API_KEY"):
    print(
        "Error: LIVEKIT_API_KEY is required. Please set it in your .env file or environment.",
        file=sys.stderr
    )
    sys.exit(1)

import asyncio
import logging
import json
from typing import Any, AsyncIterable
from typing import Annotated, Callable, Optional, cast
from pydantic import Field
from pydantic_core import from_json
from typing_extensions import TypedDict
from livekit import rtc, api
from livekit.agents import (
    AgentSession,
    Agent,
    JobContext,
    JobProcess,
    function_tool,
    RunContext,
    get_job_context,
    cli,
    WorkerOptions,
    RoomInputOptions,
    ChatContext,
    FunctionTool,
    ModelSettings,
    NOT_GIVEN,
)
from livekit.plugins import (
    deepgram,
    openai,
    cartesia,
    silero,
    noise_cancellation,  # noqa: F401
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel
from src.utils.prompt import PromptBuilder, create_agent_config_from_metadata
from src.phonenix_agent.config import AgentConfig

logger = logging.getLogger("phonenix-agent-caller")
logger.setLevel(logging.INFO)

outbound_trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")

class ResponseEmotion(TypedDict):
    voice_instructions: Annotated[
        str,
        Field(..., description="Concise TTS directive for tone, emotion, intonation, and speed"),
    ]
    response: str


async def process_structured_output(
    text: AsyncIterable[str],
    callback: Optional[Callable[[ResponseEmotion], None]] = None,
) -> AsyncIterable[str]:
    last_response = ""
    acc_text = ""
    async for chunk in text:
        acc_text += chunk
        try:
            resp: ResponseEmotion = from_json(acc_text, allow_partial="trailing-strings")
        except ValueError:
            continue

        if callback:
            callback(resp)

        if not resp.get("response"):
            continue

        new_delta = resp["response"][len(last_response) :]
        if new_delta:
            yield new_delta
        last_response = resp["response"]
class PhonenixCaller(Agent):
    def __init__(
        self,
        *,
        agent_config: AgentConfig,
        dial_info: dict[str, Any],
    ):
        # Generate dynamic prompt from configuration
        dynamic_prompt = PromptBuilder.build_prompt(agent_config)
        logger.info(f"Dynamic prompt: {dynamic_prompt}")
        super().__init__(instructions=dynamic_prompt)
        
        # keep reference to the participant for transfers
        self.participant: rtc.RemoteParticipant | None = None

        # Store configuration and dial info for use in other methods
        self.agent_config = agent_config
        self.dial_info = dial_info
        
        # Extract commonly used values for convenience
        self._user_name = agent_config.user_context.name or "Client"
        self._user_email = agent_config.user_context.email or ""
        self._call_purpose = agent_config.call_context.purpose

    def set_participant(self, participant: rtc.RemoteParticipant):
        self.participant = participant

    @staticmethod
    def prewarm(proc: JobProcess):
        proc.userdata["vad"] = silero.VAD.load()

    async def on_enter(self):
        await self.session.generate_reply(
            instructions=f"Greet {self._user_name} warmly and introduce yourself as their real estate agent. Mention that you're calling regarding {self._call_purpose} and ask how you can help them today."
        )
    async def llm_node(
        self, chat_ctx: ChatContext, tools: list[FunctionTool], model_settings: ModelSettings
    ):
        # not all LLMs support structured output, so we need to cast to the specific LLM type
        llm = cast(openai.LLM, self.llm)
        tool_choice = model_settings.tool_choice if model_settings else NOT_GIVEN
        async with llm.chat(
            chat_ctx=chat_ctx,
            tools=tools,
            tool_choice=tool_choice,
            response_format=ResponseEmotion,
        ) as stream:
            async for chunk in stream:
                yield chunk

    async def tts_node(self, text: AsyncIterable[str], model_settings: ModelSettings):
        instruction_updated = False

        def output_processed(resp: ResponseEmotion):
            nonlocal instruction_updated
            if resp.get("voice_instructions") and resp.get("response") and not instruction_updated:
                # when the response isn't empty, we can assume voice_instructions is complete.
                # (if the LLM sent the fields in the right order)
                instruction_updated = True
                logger.info(
                    f"Applying TTS instructions before generating response audio: "
                    f'"{resp["voice_instructions"]}"'
                )

                tts = cast(deepgram.TTS, self.tts)
                tts.update_options(instructions=resp["voice_instructions"])

        # process_structured_output strips the TTS instructions and only synthesizes the verbal part
        # of the LLM output
        return Agent.default.tts_node(
            self, process_structured_output(text, callback=output_processed), model_settings
        )

    async def transcription_node(self, text: AsyncIterable[str], model_settings: ModelSettings):
        # transcription_node needs to return what the agent would say, minus the TTS instructions
        return Agent.default.transcription_node(
            self, process_structured_output(text), model_settings
        )
    async def hangup(self):
        """Helper function to hang up the call by deleting the room"""

        job_ctx = get_job_context()
        await job_ctx.api.room.delete_room(
            api.DeleteRoomRequest(
                room=job_ctx.room.name,
            )
        )

    @function_tool()
    async def transfer_call(self, ctx: RunContext):
        """Transfer the call to a human agent, called after confirming with the user"""

        transfer_to = self.dial_info["transfer_to"]
        if not transfer_to:
            return "cannot transfer call"

        logger.info(f"transferring call to {transfer_to}")

        await ctx.session.generate_reply(
            instructions="let the user know you'll be transferring them to a human agent"
        )

        job_ctx = get_job_context()
        try:
            await job_ctx.api.sip.transfer_sip_participant(
                api.TransferSIPParticipantRequest(
                    room_name=job_ctx.room.name,
                    participant_identity=self.participant.identity,
                    transfer_to=f"tel:{transfer_to}",
                )
            )

            logger.info(f"transferred call to {transfer_to}")
        except Exception as e:
            logger.error(f"error transferring call: {e}")
            await ctx.session.generate_reply(
                instructions="there was an error transferring the call."
            )
            await self.hangup()

    @function_tool()
    async def end_call(self, ctx: RunContext):
        """Called when the user wants to end the call, use this tool to end the call properly"""
        participant_id = self.participant.identity if self.participant else "unknown"
        logger.info(f"ending the call for {participant_id}")
        # let the agent finish speaking
        await ctx.wait_for_playout()
        await self.hangup()

    @function_tool()
    async def schedule_property_viewing(
        self,
        ctx: RunContext,
        property_address: str,
        preferred_date: str,
        preferred_time: str,
    ):
        """Called when the user wants to schedule a property viewing

        Args:
            property_address: The address of the property to view
            preferred_date: The preferred date for the viewing
            preferred_time: The preferred time for the viewing
        """
        logger.info(
            f"scheduling property viewing for {self.participant.identity} at {property_address} on {preferred_date} at {preferred_time}"
        )
        await asyncio.sleep(2)
        return {
            "status": "viewing_scheduled",
            "property_address": property_address,
            "scheduled_date": preferred_date,
            "scheduled_time": preferred_time,
            "confirmation_number": "RE-"
            + str(hash(property_address + preferred_date + preferred_time))[
                -6:
            ].upper(),
        }

    @function_tool()
    async def schedule_consultation(
        self,
        ctx: RunContext,
        consultation_type: str,
        date: str,
        time: str,
    ):
        """Called when the user wants to schedule a real estate consultation.
        Use this tool when they want to meet to discuss their real estate needs.

        Args:
            consultation_type: The type of consultation (buying, selling, investment, etc.)
            date: The date of the consultation
            time: The time of the consultation
        """
        logger.info(
            f"scheduling {consultation_type} consultation for {self.participant.identity} on {date} at {time}"
        )
        return {
            "status": "consultation_scheduled",
            "consultation_type": consultation_type,
            "scheduled_date": date,
            "scheduled_time": time,
            "confirmation_number": "CON-"
            + str(hash(consultation_type + date + time))[-6:].upper(),
        }
    @function_tool()
    async def send_email(self, ctx: RunContext, email_to: str, subject: str, body: str):
        """Send an email to the user"""
        logger.info(f"sending email to {email_to} with subject {subject} and body {body}")
        await asyncio.sleep(1)
        return {
            "status": "email_sent",
        }

    

    @function_tool()
    async def get_property_info(
        self,
        ctx: RunContext,
        property_address: str,
    ):
        """Called when the user asks for information about a specific property

        Args:
            property_address: The address of the property to get information about
        """
        logger.info(
            f"getting property info for {self.participant.identity} about {property_address}"
        )
        await asyncio.sleep(2)
        return {
            "property_address": property_address,
            "price": "$750,000",
            "bedrooms": 3,
            "bathrooms": 2,
            "square_feet": 1800,
            "year_built": 2015,
            "property_type": "Single Family Home",
            "status": "Available",
            "description": "Beautiful modern home in a quiet neighborhood with updated kitchen and hardwood floors throughout.",
        }

    @function_tool()
    async def send_property_listings(
        self,
        ctx: RunContext,
        criteria: str,
    ):
        """Called when the user wants to receive property listings based on their criteria

        Args:
            criteria: The search criteria for properties (e.g., "3 bedroom under $500k")
        """
        logger.info(
            f"sending property listings to {self.participant.identity} based on criteria: {criteria}"
        )
        await asyncio.sleep(1)
        return {
            "status": "listings_sent",
            "criteria": criteria,
            "number_of_listings": 5,
            "delivery_method": "email",
            "message": "I've sent you 5 property listings that match your criteria. Please check your email for the details.",
        }

    @function_tool()
    async def detected_answering_machine(self, ctx: RunContext):
        """Called when the call reaches voicemail. Use this tool AFTER you hear the voicemail greeting"""
        logger.info(f"detected answering machine for {self.participant.identity}")
        await self.hangup()


async def entrypoint(ctx: JobContext):
    logger.info(f"connecting to room {ctx.room.name}")
    await ctx.connect()

    # Parse job metadata which contains all configuration
    metadata = json.loads(ctx.job.metadata)
    # Extract dial information
    dial_info = {
        "phone_number": metadata.get("phone_number"),
        "transfer_to": metadata.get("transfer_to"),
    }
    participant_identity = phone_number = dial_info["phone_number"]

    # Create agent configuration from metadata
    agent_config = create_agent_config_from_metadata(metadata)
    
    logger.info(f"Creating agent: {agent_config.agent_name} for {agent_config.company_details.name}")
    logger.info(f"Call purpose: {agent_config.call_context.purpose}")
    logger.info(f"Industry: {agent_config.industry}")

    # Create the agent with dynamic configuration
    agent = PhonenixCaller(
        agent_config=agent_config,
        dial_info=dial_info,
    )

    session = AgentSession(
        llm=openai.LLM(model="gpt-4o-mini"),
        stt=deepgram.STT(model="nova-3", language="multi"),
        tts=deepgram.TTS(),
        turn_detection=MultilingualModel(),
        vad=silero.VAD.load(),
       preemptive_generation=True,
    )

    session_started = asyncio.create_task(
        session.start(
            agent=agent,
            room=ctx.room,
            room_input_options=RoomInputOptions(
                # enable Krisp background voice and noise removal
                noise_cancellation=noise_cancellation.BVCTelephony(),
            ),
        )
    )
    # `create_sip_participant` starts dialing the user
    try:
        await ctx.api.sip.create_sip_participant(
            api.CreateSIPParticipantRequest(
                room_name=ctx.room.name,
                sip_trunk_id=outbound_trunk_id,
                sip_call_to=phone_number,
                participant_identity=participant_identity,
                # function blocks until user answers the call, or if the call fails
                wait_until_answered=True,
            )
        )

        # wait for the agent session start and participant join
        await session_started
        participant = await ctx.wait_for_participant(identity=participant_identity)
        logger.info(f"participant joined: {participant.identity}")

        agent.set_participant(participant)

    except api.TwirpError as e:
        logger.error(
            f"error creating SIP participant: {e.message}, "
            f"SIP status: {e.metadata.get('sip_status_code')} "
            f"{e.metadata.get('sip_status')}"
        )
        ctx.shutdown()


if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            agent_name="Phoenix-AI-Agent",
        )
    )
