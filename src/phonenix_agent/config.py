"""
Agent configuration classes and utilities.
Handles all agent-related configuration including personality, company details, and user context.
"""

from typing import Dict, Any, Optional, List
import json


class AgentPersonality:
    """Configuration for agent personality traits and communication style"""
    
    def __init__(
        self,
        traits: List[str],
        communication_style: str,
        tone: Optional[str] = None,
        expertise_level: Optional[str] = None,
        response_speed: Optional[str] = None,
    ):
        self.traits = traits
        self.communication_style = communication_style
        self.tone = tone or "professional"
        self.expertise_level = expertise_level or "expert"
        self.response_speed = response_speed or "conversational"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "traits": self.traits,
            "communication_style": self.communication_style,
            "tone": self.tone,
            "expertise_level": self.expertise_level,
            "response_speed": self.response_speed,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentPersonality":
        """Create from dictionary"""
        return cls(
            traits=data.get("traits", []),
            communication_style=data.get("communication_style", "professional"),
            tone=data.get("tone"),
            expertise_level=data.get("expertise_level"),
            response_speed=data.get("response_speed"),
        )


class CompanyDetails:
    """Configuration for company information and branding"""
    
    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        specialties: Optional[List[str]] = None,
        location: Optional[str] = None,
        years_in_business: Optional[int] = None,
        website: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None,
        mission_statement: Optional[str] = None,
        values: Optional[List[str]] = None,
    ):
        self.name = name
        self.description = description
        self.specialties = specialties or []
        self.location = location
        self.years_in_business = years_in_business
        self.website = website
        self.phone = phone
        self.email = email
        self.mission_statement = mission_statement
        self.values = values or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "name": self.name,
            "description": self.description,
            "specialties": self.specialties,
            "location": self.location,
            "years_in_business": self.years_in_business,
            "website": self.website,
            "phone": self.phone,
            "email": self.email,
            "mission_statement": self.mission_statement,
            "values": self.values,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CompanyDetails":
        """Create from dictionary"""
        return cls(
            name=data.get("name", ""),
            description=data.get("description"),
            specialties=data.get("specialties"),
            location=data.get("location"),
            years_in_business=data.get("years_in_business"),
            website=data.get("website"),
            phone=data.get("phone"),
            email=data.get("email"),
            mission_statement=data.get("mission_statement"),
            values=data.get("values"),
        )


class UserContext:
    """Configuration for user/client information and context"""
    
    def __init__(
        self,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        preferences: Optional[Dict[str, Any]] = None,
        previous_interactions: Optional[List[str]] = None,
        notes: Optional[str] = None,
        demographics: Optional[Dict[str, Any]] = None,
        pain_points: Optional[List[str]] = None,
        goals: Optional[List[str]] = None,
        budget: Optional[str] = None,
        timeline: Optional[str] = None,
    ):
        self.name = name
        self.email = email
        self.phone = phone
        self.preferences = preferences or {}
        self.previous_interactions = previous_interactions or []
        self.notes = notes
        self.demographics = demographics or {}
        self.pain_points = pain_points or []
        self.goals = goals or []
        self.budget = budget
        self.timeline = timeline
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "preferences": self.preferences,
            "previous_interactions": self.previous_interactions,
            "notes": self.notes,
            "demographics": self.demographics,
            "pain_points": self.pain_points,
            "goals": self.goals,
            "budget": self.budget,
            "timeline": self.timeline,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserContext":
        """Create from dictionary"""
        return cls(
            name=data.get("name"),
            email=data.get("email"),
            phone=data.get("phone"),
            preferences=data.get("preferences"),
            previous_interactions=data.get("previous_interactions"),
            notes=data.get("notes"),
            demographics=data.get("demographics"),
            pain_points=data.get("pain_points"),
            goals=data.get("goals"),
            budget=data.get("budget"),
            timeline=data.get("timeline"),
        )


class CallContext:
    """Configuration for call-specific information"""
    
    def __init__(
        self,
        purpose: str,
        priority: Optional[str] = None,
        expected_duration: Optional[str] = None,
        follow_up_required: Optional[bool] = None,
        success_metrics: Optional[List[str]] = None,
        call_script: Optional[str] = None,
        key_points: Optional[List[str]] = None,
    ):
        self.purpose = purpose
        self.priority = priority or "normal"
        self.expected_duration = expected_duration
        self.follow_up_required = follow_up_required or False
        self.success_metrics = success_metrics or []
        self.call_script = call_script
        self.key_points = key_points or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "purpose": self.purpose,
            "priority": self.priority,
            "expected_duration": self.expected_duration,
            "follow_up_required": self.follow_up_required,
            "success_metrics": self.success_metrics,
            "call_script": self.call_script,
            "key_points": self.key_points,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CallContext":
        """Create from dictionary"""
        return cls(
            purpose=data.get("purpose", ""),
            priority=data.get("priority"),
            expected_duration=data.get("expected_duration"),
            follow_up_required=data.get("follow_up_required"),
            success_metrics=data.get("success_metrics"),
            call_script=data.get("call_script"),
            key_points=data.get("key_points"),
        )


class AgentConfig:
    """Main configuration class for agent parameters"""
    
    def __init__(
        self,
        agent_name: str,
        company_details: CompanyDetails,
        agent_personality: AgentPersonality,
        call_context: CallContext,
        user_context: UserContext,
        industry: str = "real estate",
        custom_instructions: Optional[str] = None,
        language: str = "en",
        timezone: Optional[str] = None,
        compliance_requirements: Optional[List[str]] = None,
    ):
        self.agent_name = agent_name
        self.company_details = company_details
        self.agent_personality = agent_personality
        self.call_context = call_context
        self.user_context = user_context
        self.industry = industry
        self.custom_instructions = custom_instructions
        self.language = language
        self.timezone = timezone
        self.compliance_requirements = compliance_requirements or []
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        return {
            "agent_name": self.agent_name,
            "company_details": self.company_details.to_dict(),
            "agent_personality": self.agent_personality.to_dict(),
            "call_context": self.call_context.to_dict(),
            "user_context": self.user_context.to_dict(),
            "industry": self.industry,
            "custom_instructions": self.custom_instructions,
            "language": self.language,
            "timezone": self.timezone,
            "compliance_requirements": self.compliance_requirements,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AgentConfig":
        """Create from dictionary"""
        return cls(
            agent_name=data.get("agent_name", "Professional Assistant"),
            company_details=CompanyDetails.from_dict(data.get("company_details", {})),
            agent_personality=AgentPersonality.from_dict(data.get("agent_personality", {})),
            call_context=CallContext.from_dict(data.get("call_context", {})),
            user_context=UserContext.from_dict(data.get("user_context", {})),
            industry=data.get("industry", "real estate"),
            custom_instructions=data.get("custom_instructions"),
            language=data.get("language", "en"),
            timezone=data.get("timezone"),
            compliance_requirements=data.get("compliance_requirements"),
        )
    
    @classmethod
    def from_legacy_metadata(cls, metadata: Dict[str, Any]) -> "AgentConfig":
        """Create from legacy metadata format for backward compatibility"""
        
        # Extract agent configuration
        agent_config = metadata.get("agent_config", {})
        company_details = agent_config.get("company_details", {})
        agent_personality = agent_config.get("agent_personality", {})
        user_details = metadata.get("user_details", {})
        
        return cls(
            agent_name=agent_config.get("agent_name", "Professional Assistant"),
            company_details=CompanyDetails(
                name=agent_config.get("company_name", "Our Company"),
                description=company_details.get("description"),
                specialties=company_details.get("specialties"),
                location=company_details.get("location"),
                years_in_business=company_details.get("years_in_business"),
            ),
            agent_personality=AgentPersonality(
                traits=agent_personality.get("traits", ["professional", "friendly", "consultative"]),
                communication_style=agent_personality.get("communication_style", "warm and professional"),
            ),
            call_context=CallContext(
                purpose=metadata.get("call_purpose", "general inquiry"),
            ),
            user_context=UserContext(
                name=user_details.get("name"),
                email=user_details.get("email"),
                phone=user_details.get("phone"),
                preferences=user_details.get("preferences"),
                previous_interactions=user_details.get("previous_interactions"),
                notes=user_details.get("notes"),
            ),
            industry=agent_config.get("industry", "real estate"),
            custom_instructions=agent_config.get("custom_instructions"),
        )


class AgentConfigBuilder:
    """Builder class for creating agent configurations"""
    
    def __init__(self):
        self._config = {}
    
    def with_agent_name(self, name: str) -> "AgentConfigBuilder":
        """Set agent name"""
        self._config["agent_name"] = name
        return self
    
    def with_company(self, company_details: CompanyDetails) -> "AgentConfigBuilder":
        """Set company details"""
        self._config["company_details"] = company_details.to_dict()
        return self
    
    def with_personality(self, personality: AgentPersonality) -> "AgentConfigBuilder":
        """Set agent personality"""
        self._config["agent_personality"] = personality.to_dict()
        return self
    
    def with_call_context(self, call_context: CallContext) -> "AgentConfigBuilder":
        """Set call context"""
        self._config["call_context"] = call_context.to_dict()
        return self
    
    def with_user_context(self, user_context: UserContext) -> "AgentConfigBuilder":
        """Set user context"""
        self._config["user_context"] = user_context.to_dict()
        return self
    
    def with_industry(self, industry: str) -> "AgentConfigBuilder":
        """Set industry"""
        self._config["industry"] = industry
        return self
    
    def with_custom_instructions(self, instructions: str) -> "AgentConfigBuilder":
        """Set custom instructions"""
        self._config["custom_instructions"] = instructions
        return self
    
    def with_language(self, language: str) -> "AgentConfigBuilder":
        """Set language"""
        self._config["language"] = language
        return self
    
    def with_timezone(self, timezone: str) -> "AgentConfigBuilder":
        """Set timezone"""
        self._config["timezone"] = timezone
        return self
    
    def with_compliance_requirements(self, requirements: List[str]) -> "AgentConfigBuilder":
        """Set compliance requirements"""
        self._config["compliance_requirements"] = requirements
        return self
    
    def build(self) -> AgentConfig:
        """Build the final configuration"""
        return AgentConfig.from_dict(self._config)


# Predefined personality templates
class PersonalityTemplates:
    """Predefined personality templates for common agent types"""
    
    @staticmethod
    def professional_consultant() -> AgentPersonality:
        """Professional consultant personality"""
        return AgentPersonality(
            traits=["professional", "knowledgeable", "analytical", "patient"],
            communication_style="clear, consultative, and thorough",
            tone="professional",
            expertise_level="expert",
            response_speed="deliberate",
        )
    
    @staticmethod
    def friendly_sales_rep() -> AgentPersonality:
        """Friendly sales representative personality"""
        return AgentPersonality(
            traits=["friendly", "enthusiastic", "persuasive", "empathetic"],
            communication_style="warm, engaging, and solution-focused",
            tone="friendly",
            expertise_level="expert",
            response_speed="conversational",
        )
    
    @staticmethod
    def technical_expert() -> AgentPersonality:
        """Technical expert personality"""
        return AgentPersonality(
            traits=["technical", "precise", "logical", "detail-oriented"],
            communication_style="clear, technical, and data-driven",
            tone="professional",
            expertise_level="expert",
            response_speed="methodical",
        )
    
    @staticmethod
    def customer_service() -> AgentPersonality:
        """Customer service personality"""
        return AgentPersonality(
            traits=["helpful", "patient", "empathetic", "solution-oriented"],
            communication_style="warm, supportive, and problem-solving",
            tone="friendly",
            expertise_level="knowledgeable",
            response_speed="responsive",
        )


# Predefined company templates
class CompanyTemplates:
    """Predefined company templates for common industries"""
    
    @staticmethod
    def real_estate_agency() -> CompanyDetails:
        """Real estate agency template"""
        return CompanyDetails(
            name="Premier Realty Group",
            description="A leading real estate agency specializing in luxury properties",
            specialties=["luxury homes", "commercial properties", "investment properties"],
            location="San Francisco Bay Area",
            years_in_business=15,
            mission_statement="Helping clients find their perfect home",
            values=["integrity", "excellence", "client satisfaction"],
        )
    
    @staticmethod
    def insurance_company() -> CompanyDetails:
        """Insurance company template"""
        return CompanyDetails(
            name="SecureLife Insurance",
            description="Comprehensive insurance solutions for individuals and families",
            specialties=["life insurance", "health insurance", "auto insurance", "home insurance"],
            location="California",
            years_in_business=8,
            mission_statement="Protecting what matters most",
            values=["trust", "protection", "peace of mind"],
        )
    
    @staticmethod
    def financial_services() -> CompanyDetails:
        """Financial services template"""
        return CompanyDetails(
            name="WealthMax Financial",
            description="Personalized financial planning and investment management",
            specialties=["retirement planning", "investment management", "tax planning", "estate planning"],
            location="New York",
            years_in_business=12,
            mission_statement="Building wealth for a secure future",
            values=["integrity", "excellence", "client success"],
        )

