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

    def upsert_chunks(self, chunks: list[dict]) -> int:
        """Insert/update chunks by chunk_id. Returns row count written."""
        if self.admin is None:
            self.connect()
        rows = [
            {
                "chunk_id": c["chunk_id"],
                "source": c["source"],
                "text": c["text"],
                "embedding": c["embedding"],
            }
            for c in chunks
        ]
        res = self.admin.table("rag_chunks").upsert(rows, on_conflict="chunk_id").execute()
        return len(res.data or [])

    def vector_search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        min_similarity: float = 0.0,
    ) -> list[dict]:
        """Cosine similarity search via match_chunks RPC. Best first.

        Returns list of {chunk_id, source, text, similarity}.
        """
        if self.admin is None:
            self.connect()
        res = self.admin.rpc(
            "match_chunks",
            {
                "query_embedding": query_embedding,
                "match_count": top_k,
                "min_similarity": min_similarity,
            },
        ).execute()
        return res.data or []


db = DataBase()

if __name__ == "__main__":
    try:
        db.connect()
        print(f"CONNECTED clients built for {db.project_url}")
    except Exception as e:
        print(f"FAILED {e}")
