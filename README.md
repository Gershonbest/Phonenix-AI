# Phoenix AI - LiveKit Voice Agent

> Enterprise-grade AI voice automation platform for businesses seeking to reduce operational costs while improving customer service coverage.

Phoenix AI is an advanced AI telephony agent built with LiveKit, providing a dynamic voice agent service for business users. This platform enables organizations to automate customer interactions through intelligent voice agents that can handle inbound and outbound calls with natural, conversational AI.

## 🎯 Overview

Phoenix AI leverages cutting-edge AI technology to create intelligent voice agents capable of:
- **Automated Customer Service**: Handle inbound calls with human-like conversational AI
- **Proactive Outreach**: Conduct outbound calls for sales, support, and follow-ups
- **Dynamic Configuration**: Customize agent personality, company branding, and call contexts
- **Enterprise Ready**: Built for scale with LiveKit's robust infrastructure

## ✨ Key Features

### 🤖 Dynamic Agent Configuration
- **Flexible Personality System**: Configure agent traits, communication style, and expertise levels
- **Company Branding**: Customize agent responses with company details, mission, and values
- **Context-Aware**: Adapt to user context, preferences, and interaction history
- **Industry Templates**: Pre-built configurations for real estate, insurance, financial services, and more

### 📞 Advanced Call Capabilities
- **Inbound & Outbound Calls**: Support for both incoming and outgoing telephony
- **Call Transfer**: Seamlessly transfer calls to human agents when needed
- **Voice Activity Detection**: Intelligent turn-taking and conversation flow
- **Multi-language Support**: Support for multiple languages and dialects

### 🏗️ Enterprise Architecture
- **Scalable Infrastructure**: Built on LiveKit's distributed architecture
- **Noise Cancellation**: Advanced audio processing for clear conversations
- **Real-time Processing**: Low-latency voice interaction
- **Monitoring & Logging**: Comprehensive logging and monitoring capabilities

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- LiveKit account and credentials
- SIP trunk for telephony (optional, for production calls)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Phonenix-ai
   ```

2. **Install dependencies**
   ```bash
   pip install -e .
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the project root:
   ```env
   LIVEKIT_URL=your_livekit_url
   LIVEKIT_API_KEY=your_api_key
   LIVEKIT_API_SECRET=your_api_secret
   SIP_OUTBOUND_TRUNK_ID=your_trunk_id  # Optional
   ```

4. **Run the agent**
   ```bash
   python -m src.agent
   ```

## 📖 Configuration

Phoenix AI features a comprehensive configuration system for customizing agent behavior. See [CONFIGURATION_SYSTEM.md](./CONFIGURATION_SYSTEM.md) for detailed documentation.

### Basic Configuration Example

```python
from src.phonenix_agent.config import (
    AgentConfig,
    AgentPersonality,
    CompanyDetails,
    UserContext,
    CallContext,
)

# Create agent configuration
agent_config = AgentConfig(
    agent_name="Sarah",
    company_details=CompanyDetails(
        name="Premier Realty Group",
        description="Leading real estate agency",
        specialties=["luxury homes", "commercial properties"],
    ),
    agent_personality=AgentPersonality(
        traits=["professional", "friendly", "consultative"],
        communication_style="warm and professional",
    ),
    call_context=CallContext(
        purpose="Property inquiry follow-up",
    ),
    user_context=UserContext(
        name="John Doe",
        email="john@example.com",
    ),
)
```

For more examples, see [examples/agent_config_examples.py](./examples/agent_config_examples.py) and [example_configurations.json](./example_configurations.json).

## 🏗️ Architecture

```
src/
├── phonenix_agent/          # Core agent implementation
│   ├── agent.py            # Main agent class
│   ├── config.py           # Agent configuration classes
│   ├── caller/             # Call handling modules
│   │   ├── inbound.py      # Inbound call handling
│   │   └── outbound.py     # Outbound call handling
│   ├── agent_distatch/     # Agent dispatch logic
│   └── event/              # Event handling
├── config/                 # System configuration
│   ├── config.py           # Environment config
│   └── logger.py           # Logging setup
└── utils/                  # Utility modules
    └── prompt.py           # Dynamic prompt builder
```

## 📚 Documentation

- **[Configuration System](./CONFIGURATION_SYSTEM.md)**: Comprehensive guide to the agent configuration system
- **[Dynamic Prompts](./DYNAMIC_PROMPTS.md)**: Understanding how dynamic prompts are generated
- **[Examples](./examples/agent_config_examples.py)**: Code examples for various use cases

## 🔧 Development

### Running Locally

1. Set up your environment variables
2. Run the agent:
   ```bash
   python -m src.agent
   ```

### Development Dependencies

Install development dependencies:
```bash
pip install -e ".[dev]"
```

### Code Quality

The project uses:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **pytest** for testing

Format code:
```bash
black src/
isort src/
```

## 🐳 Docker

A Dockerfile is included for containerized deployment. See [Dockerfile](./Dockerfile) for details.

```bash
docker build -t phonenix-ai .
docker run -e LIVEKIT_URL=... -e LIVEKIT_API_KEY=... phonenix-ai
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For questions and support, please [add contact information or link to support channels].

---

**Phoenix AI** - Empowering businesses with intelligent voice automation.
