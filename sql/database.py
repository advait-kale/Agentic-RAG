from supabase import create_client, Client
from app.config.settings import Settings
from typing import Optional

settings = Settings()

class DataBase:
    def __init__(self):  

        self.supabase: Optional[Client] = None
        self.admin: Optional[Client] = None
        self.project_key = settings.project_url
        self.anon_key = settings.anon_public_key

    def connect(self):
        try:
            self.supabase = create_client(
                supabase_url= self.project_key,
                supabase_key= self.anon_key
            )
            self.admin = create_client(
                supabase_url= self.project_key,
                supabase_key= settings.service_role
            )
        except Exception as e:
            print(f"Error {e}")
    
