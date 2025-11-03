# Dynamic Prompt System

The Phoenix AI call agent now supports a fully dynamic prompt system that allows you to customize every aspect of the agent's behavior, personality, and knowledge base.

> **📋 New Configuration System**: This system has been enhanced with a comprehensive object-oriented configuration system. See [CONFIGURATION_SYSTEM.md](./CONFIGURATION_SYSTEM.md) for the latest features and examples.

## Features

- **Dynamic Agent Personalities**: Customize agent traits, communication style, and behavior
- **Company-Specific Information**: Include company details, specialties, and experience
- **Industry-Specific Knowledge**: Built-in knowledge for different industries (real estate, insurance, financial services, healthcare, technology)
- **User Context**: Personalized prompts based on user details, preferences, and history
- **Custom Instructions**: Add specific instructions for each call
- **Flexible Configuration**: All parameters can be passed via job metadata

## Configuration Structure

The system expects configuration data in the following format:

```json
{
  "phone_number": "+1-555-0123",
  "transfer_to": "+1-555-9999",
  "call_purpose": "Follow up on property inquiry",
  "user_details": {
    "name": "John Smith",
    "email": "john.smith@email.com",
    "phone": "+1-555-0123",
    "preferences": {
      "property_type": "single family home",
      "budget": "$1.5M - $2M"
    },
    "previous_interactions": [
      "Initial inquiry about properties",
      "Viewed 2 properties last week"
    ],
    "notes": "Interested in homes with good schools"
  },
  "agent_config": {
    "agent_name": "Sarah Johnson",
    "company_name": "Premier Realty Group",
    "company_details": {
      "description": "A leading real estate agency",
      "specialties": ["luxury homes", "commercial properties"],
      "location": "San Francisco Bay Area",
      "years_in_business": 15
    },
    "agent_personality": {
      "traits": ["professional", "knowledgeable", "patient"],
      "communication_style": "warm, consultative, and thorough"
    },
    "industry": "real estate",
    "custom_instructions": "Focus on school districts and family-friendly neighborhoods."
  }
}
```

## Configuration Parameters

### Required Parameters

- `phone_number`: The phone number to dial
- `transfer_to`: The phone number to transfer calls to
- `call_purpose`: The purpose of the call
- `agent_config.agent_name`: The name of the agent
- `agent_config.company_name`: The name of the company

### Optional Parameters

#### User Details (`user_details`)
- `name`: Client's name
- `email`: Client's email address
- `phone`: Client's phone number
- `preferences`: Object containing client preferences
- `previous_interactions`: Array of previous interaction summaries
- `notes`: Additional notes about the client

#### Agent Configuration (`agent_config`)
- `company_details`: Company information
  - `description`: Company description
  - `specialties`: Array of company specialties
  - `location`: Service area
  - `years_in_business`: Years in business
- `agent_personality`: Agent personality traits
  - `traits`: Array of personality traits
  - `communication_style`: How the agent communicates
- `industry`: Industry type (real estate, insurance, financial services, healthcare, technology)
- `custom_instructions`: Specific instructions for this call

## Supported Industries

The system includes built-in knowledge for the following industries:

1. **Real Estate**: Market knowledge, property values, buying/selling processes
2. **Insurance**: Coverage options, risk assessment, claims processes
3. **Financial Services**: Investment options, financial planning, compliance
4. **Healthcare**: Medical services, patient care, insurance coverage
5. **Technology**: Technical solutions, implementation, ROI focus

## Usage Examples

### Real Estate Agent
```python
from src.utils.prompt import AgentConfig, PromptBuilder

config = AgentConfig(
    agent_name="Sarah Johnson",
    company_name="Premier Realty Group",
    company_details={
        "description": "Luxury real estate agency",
        "specialties": ["luxury homes", "commercial properties"],
        "location": "San Francisco Bay Area"
    },
    agent_personality={
        "traits": ["professional", "knowledgeable", "patient"],
        "communication_style": "warm and consultative"
    },
    call_purpose="Follow up on property inquiry",
    user_details={
        "name": "John Smith",
        "preferences": {"budget": "$1.5M - $2M"}
    },
    industry="real estate"
)

prompt = PromptBuilder.build_prompt(config)
```

### Insurance Agent
```python
config = AgentConfig(
    agent_name="Michael Chen",
    company_name="SecureLife Insurance",
    company_details={
        "description": "Comprehensive insurance solutions",
        "specialties": ["life insurance", "health insurance"]
    },
    agent_personality={
        "traits": ["trustworthy", "analytical", "empathetic"],
        "communication_style": "clear and reassuring"
    },
    call_purpose="Policy review and coverage discussion",
    user_details={
        "name": "Lisa Rodriguez",
        "notes": "Recently had a baby, needs to update coverage"
    },
    industry="insurance"
)
```

## Testing the System

Run the test script to see different prompt configurations:

```bash
uv run python test_dynamic_prompts.py
```

This will demonstrate how different configurations generate different prompts for various industries and use cases.

## Example Configurations

See `example_configurations.json` for complete examples of different agent configurations including:

- Real Estate Agent
- Insurance Agent  
- Financial Advisor
- Technology Consultant
- Healthcare Representative

## Quick Start with New Configuration System

```python
from src.config.agent_config import AgentConfigBuilder, PersonalityTemplates, CompanyTemplates

# Create a configuration using the builder pattern
config = (
    AgentConfigBuilder()
    .with_agent_name("Sarah Johnson")
    .with_company(CompanyTemplates.real_estate_agency())
    .with_personality(PersonalityTemplates.professional_consultant())
    .with_industry("real estate")
    .with_custom_instructions("Focus on school districts and family-friendly neighborhoods")
    .build()
)

# Generate the prompt
from src.utils.prompt import PromptBuilder
prompt = PromptBuilder.build_prompt(config)
```

## Integration with LiveKit

The system integrates seamlessly with LiveKit by parsing the job metadata and creating the appropriate agent configuration. The entrypoint function automatically:

1. Parses the job metadata
2. Creates an `AgentConfig` object
3. Generates a dynamic prompt
4. Initializes the agent with the custom prompt

## Customization

You can easily extend the system by:

1. Adding new industries to the `_get_industry_knowledge()` method
2. Adding new personality traits and communication styles
3. Extending the company details format
4. Adding new user detail fields

The system is designed to be flexible and extensible while maintaining consistency across different configurations.
