from __future__ import annotations

import asyncio
import logging
from dotenv import load_dotenv
import os
from typing import Any

from livekit import rtc, api
from livekit.agents import (
    Agent,
    JobProcess,
    function_tool,
    RunContext,
    get_job_context,
)
from livekit.plugins import silero
from src.utils.prompt import PromptBuilder
from src.phonenix_agent.config import AgentConfig


# load environment variables, this is optional, only used for local development
from pathlib import Path

# Find the project root and load .env file
project_root = Path(__file__).parent.parent.parent
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)
# load_dotenv()

logger = logging.getLogger("phonenix-agent-caller")
logger.setLevel(logging.INFO)

class PhonenixCaller(Agent):
    """Phonenix AI Agent for calling clients"""
    
    def __init__(
        self,
        *,
        agent_config: AgentConfig,
        dial_info: dict[str, Any],
    ):
        # Generate dynamic prompt from configuration
        dynamic_prompt = PromptBuilder.build_prompt(agent_config)
        
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

    async def on_enter(self, ctx: RunContext):
        await ctx.session.generate_reply(
            instructions=f"Greet {self._user_name} warmly and introduce yourself as their real estate agent. Mention that you're calling regarding {self._call_purpose} and ask how you can help them today."
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
        """Called when the user wants to end the call"""
        logger.info(f"ending the call for {self.participant.identity}")

        # let the agent finish speaking
        current_speech = ctx.session.current_speech
        if current_speech:
            await current_speech.wait_for_playout()

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