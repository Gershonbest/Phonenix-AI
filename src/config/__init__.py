"""
Configuration package for Phoenix AI agent.
Contains all configuration classes and utilities for agent setup.
"""

# Re-export from phonenix_agent.config for backward compatibility
from src.phonenix_agent.config import (
    AgentConfig,
    AgentConfigBuilder,
    AgentPersonality,
    CompanyDetails,
    UserContext,
    CallContext,
    PersonalityTemplates,
    CompanyTemplates,
)

__all__ = [
    "AgentConfig",
    "AgentConfigBuilder", 
    "AgentPersonality",
    "CompanyDetails",
    "UserContext",
    "CallContext",
    "PersonalityTemplates",
    "CompanyTemplates",
]

