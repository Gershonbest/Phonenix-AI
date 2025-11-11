"""
Dynamic prompt system for AI call agents.
Supports customizable agent personalities, company details, and call purposes.
"""

from typing import Dict, Any, Optional
import json
from src.phonenix_agent.config import AgentConfig


class PromptBuilder:
    """Builder class for creating dynamic agent prompts"""

    @staticmethod
    def build_prompt(config: AgentConfig) -> str:
        """Build a comprehensive dynamic prompt from configuration"""

        # Base personality traits
        personality_traits = config.agent_personality.traits
        personality_str = (
            ", ".join(personality_traits)
            if personality_traits
            else "professional, friendly, and consultative"
        )

        # Communication style
        communication_style = config.agent_personality.communication_style
        
        # Company information
        company_info = PromptBuilder._format_company_info(config.company_details)
        
        # User information
        user_info = PromptBuilder._format_user_info(config.user_context)
        
        # Industry-specific knowledge
        industry_knowledge = PromptBuilder._get_industry_knowledge(config.industry)

        # Custom instructions
        custom_instructions = config.custom_instructions or ""

        prompt = f"""
            You are {config.agent_name}, a {personality_str} {config.industry} professional representing {config.company_details.name}. Your interface with the user is by Telephony (voice call).

            {company_info}

            {user_info}

            Call Purpose: {config.call_context.purpose}

            Personality & Communication Style:
            - You are {communication_style}
            - {personality_str.replace(',', ' and')} in your approach
            - Focused on understanding the client's needs and providing value
            - Respectful of their time and preferences

            {industry_knowledge}

            Your goal is to engage with the client about their {config.industry} needs and provide helpful information or schedule follow-up activities as appropriate.
            Always be polite and professional. Allow the user to end the conversation when they're ready.

            Available Tools (use when appropriate):
            - end_call: **MOST IMPORTANT** - Call this when the user wants to end the call, says goodbye, or conversation is complete. ALWAYS call this to properly end calls.
            - transfer_call: Transfer to a human agent after confirming with user, then call end_call.
            - schedule_property_viewing: Schedule a property viewing when user requests it (needs: property_address, preferred_date, preferred_time).
            - schedule_consultation: Schedule a consultation meeting when user wants to meet (needs: consultation_type, date, time).
            - send_email: Send email to user when requested or for follow-up materials (needs: email_to, subject, body).
            - get_property_info: Get property details when user asks about a specific property (needs: property_address).
            - send_property_listings: Send property listings matching user's search criteria (needs: criteria).
            - detected_answering_machine: Call when you detect voicemail AFTER hearing the greeting.

            {custom_instructions}
        """.strip()

        return prompt

    @staticmethod
    def _format_company_info(company_details) -> str:
        """Format company information for the prompt"""
        if not company_details:
            return ""

        info_parts = []

        if company_details.description:
            info_parts.append(f"Company Description: {company_details.description}")

        if company_details.specialties:
            specialties_str = ", ".join(company_details.specialties)
            info_parts.append(f"Company Specialties: {specialties_str}")

        if company_details.location:
            info_parts.append(f"Service Area: {company_details.location}")

        if company_details.years_in_business:
            info_parts.append(
                f"Experience: {company_details.years_in_business} years in business"
            )

        if company_details.mission_statement:
            info_parts.append(f"Mission: {company_details.mission_statement}")

        if company_details.values:
            values_str = ", ".join(company_details.values)
            info_parts.append(f"Company Values: {values_str}")

        return "\n".join(info_parts) if info_parts else ""

    @staticmethod
    def _format_user_info(user_context) -> str:
        """Format user information for the prompt"""
        if not user_context:
            return ""

        info_parts = []

        if user_context.name:
            info_parts.append(f"Client Name: {user_context.name}")

        if user_context.email:
            info_parts.append(f"Client Email: {user_context.email}")

        if user_context.phone:
            info_parts.append(f"Client Phone: {user_context.phone}")

        if user_context.preferences:
            info_parts.append(
                f"Client Preferences: {json.dumps(user_context.preferences)}"
            )

        if user_context.previous_interactions:
            info_parts.append(
                f"Previous Interactions: {json.dumps(user_context.previous_interactions)}"
            )

        if user_context.notes:
            info_parts.append(f"Additional Notes: {user_context.notes}")

        if user_context.goals:
            goals_str = ", ".join(user_context.goals)
            info_parts.append(f"Client Goals: {goals_str}")

        if user_context.budget:
            info_parts.append(f"Budget: {user_context.budget}")

        if user_context.timeline:
            info_parts.append(f"Timeline: {user_context.timeline}")

        return "\n".join(info_parts) if info_parts else ""

    @staticmethod
    def _get_industry_knowledge(industry: str) -> str:
        """Get industry-specific knowledge and guidelines"""
        knowledge_map = {
            "real estate": """
                Industry Knowledge:
                - Knowledgeable about the local real estate market
                - Understand property values, market trends, and neighborhood insights
                - Familiar with buying/selling processes, financing options, and legal requirements
                - Can provide market analysis and property recommendations
                """,
            "insurance": """
                Industry Knowledge:
                - Knowledgeable about various insurance products and coverage options
                - Understand risk assessment and policy customization
                - Familiar with claims processes and customer protection
                - Can provide quotes and explain coverage benefits
                """,
            "financial services": """
                Industry Knowledge:
                - Knowledgeable about financial products and investment options
                - Understand market conditions and financial planning
                - Familiar with regulatory requirements and compliance
                - Can provide financial advice and product recommendations
                """,
            "healthcare": """
                Industry Knowledge:
                - Knowledgeable about healthcare services and treatment options
                - Understand patient care and medical procedures
                - Familiar with insurance coverage and billing processes
                - Can provide information about appointments and services
                """,
            "default": """
                Industry Knowledge:
                - Knowledgeable about your industry and market
                - Professional and consultative in your approach
                - Focused on understanding client needs and providing value
                """,
        }

        return knowledge_map.get(industry, knowledge_map["default"])


def create_agent_config_from_metadata(metadata: Dict[str, Any]) -> AgentConfig:
    """Create AgentConfig from job metadata"""
    return AgentConfig.from_legacy_metadata(metadata)


# Legacy function for backward compatibility
def get_prompt(
    agent_name,
    user_preferences,
    user_needs,
    user_goals,
    user_concerns,
    user_feedback,
    user_history,
):
    """Legacy function - use PromptBuilder.build_prompt() instead"""
    config = AgentConfig(
        agent_name=agent_name,
        company_name="Our Company",
        company_details={},
        agent_personality={
            "traits": ["warm", "empathetic", "human-like"],
            "communication_style": "natural with genuine emotions",
        },
        call_purpose="general assistance",
        user_details={
            "preferences": user_preferences,
            "needs": user_needs,
            "goals": user_goals,
            "concerns": user_concerns,
            "feedback": user_feedback,
            "history": user_history,
        },
    )
    return PromptBuilder.build_prompt(config)
