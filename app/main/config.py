import os
from dotenv import load_dotenv

load_dotenv() 

class Config:
    DEBUG = False

    # LLM Config
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")

class DevConfig(Config):
    DEBUG = True
    # MongoDB Config
    
    MONGO_DATABASE_NAME = os.getenv("MONGO_DATABASE_NAME", "agentic_ai_db")
    # MONGO_DATABASE_USERNAME = os.getenv("MONGO_DATABASE_USERNAME", "")
    # MONGO_DATABASE_PASSWORD = os.getenv("MONGO_DATABASE_PASSWORD", "")
    MONGO_DATABASE_HOST = os.getenv("MONGO_DATABASE_HOST", "localhost")
    MONGO_DATABASE_PORT = int(os.getenv("MONGO_DATABASE_PORT", 27017))

class ProdConfig(Config):
    #---------------- these credentials will be for prod as of now, we are not adding anything here, will add at the time of deployment.
    pass

config_by_name = dict(dev=DevConfig, prod=ProdConfig)


def get_config_by_name(config_name, default=None, env_param_name=None):
    config_env = os.getenv(env_param_name or "ENV") or "dev"
    config_value = default
    if config_env:
        config_value = getattr(config_by_name[config_env](), config_name, default)
    return config_value