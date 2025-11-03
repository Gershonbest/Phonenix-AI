# Agent Configuration System

The Phoenix AI agent now features a comprehensive, object-oriented configuration system that provides maximum flexibility and maintainability for creating dynamic agent prompts.

## 🏗️ Architecture

The configuration system is built with a modular, object-oriented approach:

```
src/config/
├── __init__.py
└── agent_config.py          # Core configuration classes
```

### Core Classes

- **`AgentConfig`** - Main configuration container
- **`AgentPersonality`** - Agent personality and communication style
- **`CompanyDetails`** - Company information and branding
- **`UserContext`** - Client/user information and context
- **`CallContext`** - Call-specific information and objectives
- **`AgentConfigBuilder`** - Fluent builder pattern for easy configuration
- **`PersonalityTemplates`** - Predefined personality types
- **`CompanyTemplates`** - Predefined company templates

## 🚀 Key Features

### 1. **Object-Oriented Design**
- Type-safe configuration with proper validation
- Clear separation of concerns
- Easy to extend and maintain

### 2. **Builder Pattern**
- Fluent API for easy configuration
- Method chaining for readable code
- Flexible and intuitive

### 3. **Predefined Templates**
- Common personality types (professional, friendly, technical, etc.)
- Industry-specific company templates
- Quick setup for common use cases

### 4. **Serialization Support**
- Convert configurations to/from dictionaries
- Easy storage and retrieval
- API integration ready

### 5. **Backward Compatibility**
- Legacy metadata format still supported
- Gradual migration path
- No breaking changes

## 📋 Usage Examples

### Basic Configuration

```python
from src.config.agent_config import (
    AgentConfig, AgentPersonality, CompanyDetails, 
    UserContext, CallContext
)

# Create individual components
company = CompanyDetails(
    name="Premier Realty Group",
    description="Luxury real estate agency",
    specialties=["luxury homes", "commercial properties"],
    location="San Francisco Bay Area",
    years_in_business=15
)

personality = AgentPersonality(
    traits=["professional", "knowledgeable", "patient"],
    communication_style="warm, consultative, and thorough"
)

call_context = CallContext(
    purpose="Follow up on property inquiry",
    priority="high",
    success_metrics=["schedule viewing", "gather requirements"]
)

user_context = UserContext(
    name="John Smith",
    email="john.smith@email.com",
    preferences={"budget": "$1.5M - $2M"},
    goals=["find family home", "good school district"]
)

# Create agent configuration
config = AgentConfig(
    agent_name="Sarah Johnson",
    company_details=company,
    agent_personality=personality,
    call_context=call_context,
    user_context=user_context,
    industry="real estate",
    custom_instructions="Focus on school districts"
)
```

### Builder Pattern

```python
from src.config.agent_config import AgentConfigBuilder, CompanyDetails, AgentPersonality

config = (
    AgentConfigBuilder()
    .with_agent_name("Michael Chen")
    .with_company(
        CompanyDetails(
            name="SecureLife Insurance",
            description="Comprehensive insurance solutions",
            specialties=["life insurance", "health insurance"]
        )
    )
    .with_personality(
        AgentPersonality(
            traits=["trustworthy", "analytical", "empathetic"],
            communication_style="clear and reassuring"
        )
    )
    .with_industry("insurance")
    .with_custom_instructions("Emphasize family protection benefits")
    .build()
)
```

### Using Templates

```python
from src.config.agent_config import (
    AgentConfigBuilder, PersonalityTemplates, CompanyTemplates
)

config = (
    AgentConfigBuilder()
    .with_agent_name("David Thompson")
    .with_company(CompanyTemplates.financial_services())
    .with_personality(PersonalityTemplates.professional_consultant())
    .with_industry("financial services")
    .build()
)
```

### Serialization

```python
# Convert to dictionary
config_dict = config.to_dict()

# Convert from dictionary
restored_config = AgentConfig.from_dict(config_dict)

# Legacy metadata compatibility
from src.utils.prompt import create_agent_config_from_metadata
config = create_agent_config_from_metadata(legacy_metadata)
```

## 🎭 Personality Templates

### Available Templates

- **`professional_consultant()`** - Professional, analytical, patient
- **`friendly_sales_rep()`** - Friendly, enthusiastic, persuasive
- **`technical_expert()`** - Technical, precise, logical
- **`customer_service()`** - Helpful, patient, empathetic

### Custom Personalities

```python
personality = AgentPersonality(
    traits=["creative", "innovative", "collaborative"],
    communication_style="energetic and solution-focused",
    tone="casual",
    expertise_level="expert",
    response_speed="quick"
)
```

## 🏢 Company Templates

### Available Templates

- **`real_estate_agency()`** - Premier Realty Group
- **`insurance_company()`** - SecureLife Insurance  
- **`financial_services()`** - WealthMax Financial

### Custom Companies

```python
company = CompanyDetails(
    name="TechSolutions Inc",
    description="Leading technology consulting firm",
    specialties=["cloud migration", "digital transformation"],
    location="Austin, Texas",
    years_in_business=10,
    mission_statement="Transforming businesses through technology",
    values=["innovation", "excellence", "collaboration"]
)
```

## 📊 Configuration Structure

### AgentConfig Properties

```python
config.agent_name                    # str: Agent's name
config.company_details              # CompanyDetails: Company info
config.agent_personality            # AgentPersonality: Personality traits
config.call_context                 # CallContext: Call information
config.user_context                 # UserContext: Client information
config.industry                     # str: Industry type
config.custom_instructions          # str: Custom instructions
config.language                     # str: Language (default: "en")
config.timezone                     # str: Timezone
config.compliance_requirements      # List[str]: Compliance rules
```

### CompanyDetails Properties

```python
company.name                        # str: Company name
company.description                 # str: Company description
company.specialties                 # List[str]: Company specialties
company.location                    # str: Service area
company.years_in_business           # int: Years in business
company.website                     # str: Company website
company.phone                       # str: Company phone
company.email                       # str: Company email
company.mission_statement           # str: Mission statement
company.values                      # List[str]: Company values
```

### AgentPersonality Properties

```python
personality.traits                  # List[str]: Personality traits
personality.communication_style     # str: Communication style
personality.tone                    # str: Tone (professional, friendly, etc.)
personality.expertise_level         # str: Expertise level
personality.response_speed          # str: Response speed
```

### UserContext Properties

```python
user.name                           # str: Client name
user.email                          # str: Client email
user.phone                          # str: Client phone
user.preferences                    # Dict: Client preferences
user.previous_interactions          # List[str]: Previous interactions
user.notes                          # str: Additional notes
user.demographics                   # Dict: Demographics
user.pain_points                    # List[str]: Pain points
user.goals                          # List[str]: Client goals
user.budget                         # str: Budget information
user.timeline                       # str: Timeline
```

### CallContext Properties

```python
call.purpose                        # str: Call purpose
call.priority                       # str: Priority level
call.expected_duration              # str: Expected duration
call.follow_up_required             # bool: Follow-up needed
call.success_metrics                # List[str]: Success metrics
call.call_script                    # str: Call script
call.key_points                     # List[str]: Key points to cover
```

## 🔄 Migration Guide

### From Legacy System

The new system is fully backward compatible. Legacy metadata will be automatically converted:

```python
# Old way (still works)
metadata = {
    "agent_config": {
        "agent_name": "Sarah Johnson",
        "company_name": "Premier Realty Group",
        "company_details": {...},
        "agent_personality": {...}
    },
    "call_purpose": "Follow up on inquiry",
    "user_details": {...}
}

config = create_agent_config_from_metadata(metadata)
```

### To New System

```python
# New way (recommended)
config = (
    AgentConfigBuilder()
    .with_agent_name("Sarah Johnson")
    .with_company(CompanyDetails(name="Premier Realty Group", ...))
    .with_personality(AgentPersonality(traits=[...], ...))
    .build()
)
```

## 🧪 Testing

Run the examples to see the system in action:

```bash
uv run python examples/agent_config_examples.py
```

This will demonstrate:
1. Basic configuration creation
2. Builder pattern usage
3. Template usage
4. Serialization/deserialization
5. Legacy compatibility

## 🎯 Benefits

### For Developers
- **Type Safety**: Catch configuration errors at development time
- **IntelliSense**: Full IDE support with autocomplete
- **Maintainability**: Clear, organized code structure
- **Extensibility**: Easy to add new features

### For Users
- **Flexibility**: Configure any aspect of the agent
- **Consistency**: Standardized configuration format
- **Reusability**: Templates and builders for common patterns
- **Reliability**: Validated configurations prevent runtime errors

### For Operations
- **Serialization**: Easy storage and retrieval
- **Versioning**: Track configuration changes
- **Validation**: Ensure configurations are complete
- **Documentation**: Self-documenting configuration structure

## 🔮 Future Enhancements

- **Configuration Validation**: Schema validation for configurations
- **Configuration UI**: Web interface for creating configurations
- **A/B Testing**: Support for configuration experiments
- **Analytics**: Track configuration performance
- **Templates Library**: Community-shared configuration templates

The new configuration system provides a solid foundation for building sophisticated, dynamic AI agents while maintaining simplicity and ease of use.

