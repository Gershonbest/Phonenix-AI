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
class InboundCall:
    """InboundCall class for handling inbound calls"""

    def __init__(self, phone_number: str, ctx: JobContext):
        """Initialize the InboundCall"""

        self.phone_number = phone_number
        self.ctx = ctx