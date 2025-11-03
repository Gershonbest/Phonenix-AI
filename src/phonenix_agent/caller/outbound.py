from __future__ import annotations

import asyncio
import logging
from dotenv import load_dotenv
import json
import os
from typing import Any

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

from src.config.logger import Logger
logger = Logger("OutboundCaller").get_logger()


class OutboundCaller:
    """OutboundCaller class for making outbound calls"""

    def __init__(self, phone_number: str, ctx: JobContext):
        """Initialize the OutboundCaller"""

        self.phone_number = phone_number
        self.ctx = ctx
        self.session = AgentSession(
            llm=openai.LLM(model="gpt-4o-mini"),
            stt=deepgram.STT(model="nova-3", language="multi"),
            tts=deepgram.TTS(),
            turn_detection=MultilingualModel(),
            vad=silero.VAD.load(),
            preemptive_generation=True,
        )
        self.participant_identity = f"participant_{phone_number}"
        self.outbound_trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")
        logger.info(f"OutboundCaller initialized for {phone_number}")
        self.session_started = asyncio.create_task(
            self.session.start(
                agent=self,
                room=self.ctx.room,
                room_input_options=RoomInputOptions(
                    noise_cancellation=noise_cancellation.BVCTelephony(),
                ),
            )
        )

    def set_participant(self, participant: rtc.RemoteParticipant):
        self.participant = participant
    async def call(self):
        await self.outbound_call(self.phone_number, self.ctx, self.participant_identity, self.outbound_trunk_id)

    async def outbound_call(self, phone_number: str, ctx: JobContext, participant_identity: str, outbound_trunk_id: str):
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
            await self.session_started
            participant = await ctx.wait_for_participant(identity=participant_identity)
            logger.info(f"participant joined: {participant.identity}")

            self.set_participant(participant)

        except api.TwirpError as e:
            logger.error(
                f"error creating SIP participant: {e.message}, "
                f"SIP status: {e.metadata.get('sip_status_code')} "
                f"{e.metadata.get('sip_status')}"
            )
            ctx.shutdown()