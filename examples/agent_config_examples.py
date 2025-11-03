#!/usr/bin/env python3
"""
Examples demonstrating how to use the new agent configuration system.
Shows different ways to create and configure agents.
"""

from src.config import (
    AgentConfig,
    AgentConfigBuilder,
    AgentPersonality,
    CompanyDetails,
    UserContext,
    CallContext,
    PersonalityTemplates,
    CompanyTemplates,
)
from src.utils.prompt import PromptBuilder


def example_1_basic_configuration():
    """Example 1: Basic configuration using individual classes"""
    print("=" * 80)
    print("EXAMPLE 1: Basic Configuration")
    print("=" * 80)
    
    # Create company details
    company = CompanyDetails(
        name="Premier Realty Group",
        description="A leading real estate agency specializing in luxury properties",
        specialties=["luxury homes", "commercial properties", "investment properties"],
        location="San Francisco Bay Area",
        years_in_business=15,
        mission_statement="Helping clients find their perfect home",
        values=["integrity", "excellence", "client satisfaction"],
    )
    
    # Create agent personality
    personality = AgentPersonality(
        traits=["professional", "knowledgeable", "patient", "detail-oriented"],
        communication_style="warm, consultative, and thorough",
        tone="professional",
        expertise_level="expert",
        response_speed="conversational",
    )
    
    # Create call context
    call_context = CallContext(
        purpose="Follow up on property inquiry for 3-bedroom home in Palo Alto",
        priority="high",
        expected_duration="15-20 minutes",
        follow_up_required=True,
        success_metrics=["schedule viewing", "gather requirements", "build rapport"],
        key_points=["school districts", "family-friendly neighborhoods", "upcoming open houses"],
    )
    
    # Create user context
    user_context = UserContext(
        name="John Smith",
        email="john.smith@email.com",
        phone="+1-555-0123",
        preferences={
            "property_type": "single family home",
            "budget": "$1.5M - $2M",
            "location": "Palo Alto or nearby",
        },
        previous_interactions=[
            "Initial inquiry about Palo Alto properties",
            "Viewed 2 properties last week",
        ],
        notes="Interested in homes with good schools nearby",
        goals=["find family home", "good school district", "move by summer"],
        budget="$1.5M - $2M",
        timeline="3-6 months",
    )
    
    # Create agent configuration
    config = AgentConfig(
        agent_name="Sarah Johnson",
        company_details=company,
        agent_personality=personality,
        call_context=call_context,
        user_context=user_context,
        industry="real estate",
        custom_instructions="Focus on school districts and family-friendly neighborhoods. Mention upcoming open houses.",
        language="en",
        timezone="America/Los_Angeles",
    )
    
    # Generate prompt
    prompt = PromptBuilder.build_prompt(config)
    print(prompt)
    print("\n")


def example_2_using_builder():
    """Example 2: Using the builder pattern"""
    print("=" * 80)
    print("EXAMPLE 2: Using Builder Pattern")
    print("=" * 80)
    
    config = (
        AgentConfigBuilder()
        .with_agent_name("Michael Chen")
        .with_company(
            CompanyDetails(
                name="SecureLife Insurance",
                description="Comprehensive insurance solutions for individuals and families",
                specialties=["life insurance", "health insurance", "auto insurance"],
                location="California",
                years_in_business=8,
            )
        )
        .with_personality(
            AgentPersonality(
                traits=["trustworthy", "analytical", "empathetic", "solution-focused"],
                communication_style="clear, reassuring, and educational",
            )
        )
        .with_call_context(
            CallContext(
                purpose="Review current policy and discuss coverage options",
                priority="normal",
                follow_up_required=True,
            )
        )
        .with_user_context(
            UserContext(
                name="Lisa Rodriguez",
                email="lisa.rodriguez@email.com",
                notes="Recently had a baby, needs to update coverage",
                goals=["protect family", "update coverage", "save money"],
            )
        )
        .with_industry("insurance")
        .with_custom_instructions("Emphasize family protection benefits and new parent discounts.")
        .build()
    )
    
    prompt = PromptBuilder.build_prompt(config)
    print(prompt)
    print("\n")


def example_3_using_templates():
    """Example 3: Using predefined templates"""
    print("=" * 80)
    print("EXAMPLE 3: Using Predefined Templates")
    print("=" * 80)
    
    config = (
        AgentConfigBuilder()
        .with_agent_name("David Thompson")
        .with_company(CompanyTemplates.financial_services())
        .with_personality(PersonalityTemplates.professional_consultant())
        .with_call_context(
            CallContext(
                purpose="Quarterly portfolio review and retirement planning discussion",
                priority="high",
                success_metrics=["review performance", "adjust strategy", "plan contributions"],
            )
        )
        .with_user_context(
            UserContext(
                name="Robert Kim",
                email="robert.kim@email.com",
                notes="Recently received promotion, wants to increase contributions",
                goals=["retire at 65", "increase savings", "tax optimization"],
                budget="$500-1000/month additional",
            )
        )
        .with_industry("financial services")
        .with_custom_instructions("Discuss increased contribution options and tax-advantaged accounts.")
        .build()
    )
    
    prompt = PromptBuilder.build_prompt(config)
    print(prompt)
    print("\n")


def example_4_serialization():
    """Example 4: Serialization and deserialization"""
    print("=" * 80)
    print("EXAMPLE 4: Serialization and Deserialization")
    print("=" * 80)
    
    # Create a configuration
    original_config = (
        AgentConfigBuilder()
        .with_agent_name("Alex Martinez")
        .with_company(
            CompanyDetails(
                name="TechSolutions Inc",
                description="Leading technology consulting firm",
                specialties=["cloud migration", "digital transformation"],
                location="Austin, Texas",
            )
        )
        .with_personality(PersonalityTemplates.technical_expert())
        .with_call_context(
            CallContext(
                purpose="Follow up on cloud migration proposal",
                priority="high",
            )
        )
        .with_user_context(
            UserContext(
                name="Jane Doe",
                email="jane.doe@email.com",
                notes="CTO is interested but needs ROI justification",
                goals=["cloud migration", "cost reduction", "scalability"],
            )
        )
        .with_industry("technology")
        .build()
    )
    
    # Serialize to dictionary
    config_dict = original_config.to_dict()
    print("Serialized configuration:")
    print(f"Agent Name: {config_dict['agent_name']}")
    print(f"Company: {config_dict['company_details']['name']}")
    print(f"Industry: {config_dict['industry']}")
    print()
    
    # Deserialize from dictionary
    restored_config = AgentConfig.from_dict(config_dict)
    
    # Generate prompt from restored configuration
    prompt = PromptBuilder.build_prompt(restored_config)
    print("Generated prompt from restored configuration:")
    print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
    print("\n")


def example_5_legacy_compatibility():
    """Example 5: Legacy metadata compatibility"""
    print("=" * 80)
    print("EXAMPLE 5: Legacy Metadata Compatibility")
    print("=" * 80)
    
    # Legacy metadata format
    legacy_metadata = {
        "phone_number": "+1-555-0123",
        "transfer_to": "+1-555-9999",
        "call_purpose": "Follow up on service inquiry",
        "user_details": {
            "name": "Jane Doe",
            "email": "jane.doe@email.com",
            "preferences": {"service_type": "premium"},
        },
        "agent_config": {
            "agent_name": "Alex Martinez",
            "company_name": "TechSolutions Inc",
            "company_details": {
                "description": "Leading technology consulting firm",
                "specialties": ["cloud migration", "digital transformation"],
                "location": "Austin, Texas",
            },
            "agent_personality": {
                "traits": ["technical", "innovative", "collaborative"],
                "communication_style": "clear and solution-oriented",
            },
            "industry": "technology",
            "custom_instructions": "Focus on ROI and implementation timeline.",
        },
    }
    
    # Convert legacy metadata to new configuration
    from src.utils.prompt import create_agent_config_from_metadata
    
    config = create_agent_config_from_metadata(legacy_metadata)
    
    print("Converted from legacy metadata:")
    print(f"Agent: {config.agent_name}")
    print(f"Company: {config.company_details.name}")
    print(f"Industry: {config.industry}")
    print(f"Call Purpose: {config.call_context.purpose}")
    print()
    
    # Generate prompt
    prompt = PromptBuilder.build_prompt(config)
    print("Generated prompt:")
    print(prompt[:300] + "..." if len(prompt) > 300 else prompt)
    print("\n")


if __name__ == "__main__":
    print("AGENT CONFIGURATION SYSTEM EXAMPLES")
    print("This script demonstrates different ways to configure agents.\n")
    
    example_1_basic_configuration()
    example_2_using_builder()
    example_3_using_templates()
    example_4_serialization()
    example_5_legacy_compatibility()
    
    print("=" * 80)
    print("All examples completed successfully!")
    print("=" * 80)

