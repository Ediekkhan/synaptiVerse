"""
Environment configuration loader for SynaptiVerse
Loads and validates environment variables from .env file
"""

import os
from typing import Optional
from pathlib import Path


class Config:
    """Configuration management using environment variables"""
    
    # Base directory
    BASE_DIR = Path(__file__).parent.parent
    
    # Server Configuration
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    
    # Fetch.ai Agent Configuration
    COORDINATOR_SEED: str = os.getenv("COORDINATOR_SEED", "synaptiverse_coordinator_default")
    ADVISOR_SEED: str = os.getenv("ADVISOR_SEED", "synaptiverse_advisor_default")
    AGENTVERSE_ENABLED: bool = os.getenv("AGENTVERSE_ENABLED", "False").lower() == "true"
    AGENTVERSE_MAILBOX_KEY: Optional[str] = os.getenv("AGENTVERSE_MAILBOX_KEY")
    AGENTVERSE_API_KEY: Optional[str] = os.getenv("AGENTVERSE_API_KEY")
    
    # MeTTa Configuration
    METTA_KNOWLEDGE_PATH: str = os.getenv("METTA_KNOWLEDGE_PATH", "src/metta/knowledge_graphs/medical_facts.metta")
    METTA_CACHE_ENABLED: bool = os.getenv("METTA_CACHE_ENABLED", "True").lower() == "true"
    METTA_MAX_FACTS: int = int(os.getenv("METTA_MAX_FACTS", "1000"))
    
    # API Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", "http://localhost:8000").split(",")
    CORS_ALLOW_CREDENTIALS: bool = os.getenv("CORS_ALLOW_CREDENTIALS", "True").lower() == "true"
    RATE_LIMIT_ENABLED: bool = os.getenv("RATE_LIMIT_ENABLED", "False").lower() == "true"
    RATE_LIMIT_REQUESTS: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    RATE_LIMIT_PERIOD: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    
    # Healthcare Configuration
    DEFAULT_APPOINTMENT_DURATION: int = int(os.getenv("DEFAULT_APPOINTMENT_DURATION", "30"))
    TIMEZONE: str = os.getenv("TIMEZONE", "UTC")
    EMERGENCY_NOTIFICATION_ENABLED: bool = os.getenv("EMERGENCY_NOTIFICATION_ENABLED", "False").lower() == "true"
    EMERGENCY_WEBHOOK_URL: Optional[str] = os.getenv("EMERGENCY_WEBHOOK_URL")
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = os.getenv("LOG_FORMAT", "text")
    LOG_FILE: str = os.getenv("LOG_FILE", "logs/synaptiverse.log")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "insecure_default_key_change_in_production")
    STORE_PHI: bool = os.getenv("STORE_PHI", "False").lower() == "true"
    ENABLE_ANALYTICS: bool = os.getenv("ENABLE_ANALYTICS", "False").lower() == "true"
    
    # Testing
    TEST_MODE: bool = os.getenv("TEST_MODE", "False").lower() == "true"
    MOCK_AGENTS: bool = os.getenv("MOCK_AGENTS", "False").lower() == "true"
    
    @classmethod
    def load_env_file(cls, env_file: str = ".env") -> None:
        """Load environment variables from .env file"""
        env_path = cls.BASE_DIR / env_file
        
        if not env_path.exists():
            print(f"⚠️  Warning: {env_file} not found. Using default configuration.")
            return
        
        try:
            with open(env_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    # Skip comments and empty lines
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse KEY=VALUE
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Only set if not already in environment
                        if key and not os.getenv(key):
                            os.environ[key] = value
            
            print(f"✅ Loaded configuration from {env_file}")
        except Exception as e:
            print(f"❌ Error loading {env_file}: {e}")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required configuration"""
        errors = []
        
        # Check for insecure defaults in production
        if cls.ENVIRONMENT == "production":
            if cls.SECRET_KEY == "insecure_default_key_change_in_production":
                errors.append("SECRET_KEY must be changed in production")
            
            if cls.DEBUG:
                errors.append("DEBUG should be False in production")
            
            if "localhost" in ",".join(cls.CORS_ORIGINS):
                errors.append("CORS_ORIGINS should not include localhost in production")
        
        # Check privacy settings
        if cls.STORE_PHI:
            errors.append("STORE_PHI must be False to maintain privacy-first architecture")
        
        # Log errors
        if errors:
            print("❌ Configuration validation failed:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        print("✅ Configuration validated successfully")
        return True
    
    @classmethod
    def print_config(cls) -> None:
        """Print current configuration (excluding secrets)"""
        print("\n" + "="*60)
        print("SYNAPTIVERSE CONFIGURATION")
        print("="*60)
        print(f"Environment: {cls.ENVIRONMENT}")
        print(f"Debug Mode: {cls.DEBUG}")
        print(f"Server: {cls.HOST}:{cls.PORT}")
        print(f"MeTTa Facts: {cls.METTA_MAX_FACTS}")
        print(f"Agent Seeds: {cls.COORDINATOR_SEED[:20]}..., {cls.ADVISOR_SEED[:20]}...")
        print(f"Agentverse: {'Enabled' if cls.AGENTVERSE_ENABLED else 'Disabled'}")
        print(f"PHI Storage: {'ENABLED (INSECURE!)' if cls.STORE_PHI else 'Disabled (Privacy-First)'}")
        print(f"Log Level: {cls.LOG_LEVEL}")
        print("="*60 + "\n")


# Auto-load .env file on module import
Config.load_env_file()


# Example usage in other modules:
# from config import Config
# print(Config.PORT)
# if Config.DEBUG: ...
