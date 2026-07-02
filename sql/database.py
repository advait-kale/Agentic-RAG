from supabase import create_client, Client
from app.config.settings import Settings
from typing import Optional

settings = Settings()


class DataBase:
    def __init__(self):
        self.supabase: Optional[Client] = None   # anon
        self.admin: Optional[Client] = None       # service_role
        self.project_url = settings.project_url
        self.anon_key = settings.anon_public_key

    def connect(self):
        self.supabase = create_client(
            supabase_url=self.project_url,
            supabase_key=self.anon_key,
        )
        self.admin = create_client(
            supabase_url=self.project_url,
            supabase_key=settings.service_role,
        )


db = DataBase()

if __name__ == "__main__":
    try:
        db.connect()
        print(f"CONNECTED clients built for {db.project_url}")
    except Exception as e:
        print(f"FAILED {e}")
