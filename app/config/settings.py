from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    #embedding.py
    embedding_model: str = "qwen3-embedding:0.6b"

    #chat.py
    llm_model: str = "qwen3:8b"
    llm_provider: str = "ollama"

    #SupaBase Configs
    project_url: str = "https://xpieiqppxhmwtxdgmhua.supabase.co"
    anon_public_key: str          # from .env ANON_PUBLIC_KEY
    service_role: str             # from .env SERVICE_ROLE  (secret)

    # Email  (from .env)
    email_address: str            # EMAIL_ADDRESS
    app_password: str             # APP_PASSWORD  (secret)

setting = Settings()

def get_settings() -> Settings:
    return setting
