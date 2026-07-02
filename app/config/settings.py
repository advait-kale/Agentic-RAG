from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    #embedding.py
    embedding_model:str = "qwen3-embedding:0.6b"

    #chat.py
    llm_model:str = "qwen3:8b"
    llm_provider:str = "ollama"

    #SupaBase Configs

    project_url = "https://xpieiqppxhmwtxdgmhua.supabase.co/rest/v1/"
    anon_public_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhwaWVpcXBweGhtd3R4ZGdtaHVhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODI5OTY5MTQsImV4cCI6MjA5ODU3MjkxNH0.8M5GRIgvyihv4tzmdtPOegd78fuXuQZeJD0mkhxWGfg"
    #secret
    service_role = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhwaWVpcXBweGhtd3R4ZGdtaHVhIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc4Mjk5NjkxNCwiZXhwIjoyMDk4NTcyOTE0fQ.MEM76aB9Qksn-Nidd7Qm5DJy_AJ_9qHC2MjUmTp0aKA" 

