from app.services.embeddings import embedding
from app.services.chat import chat
from sql.database import db
from typing import List, Dict
from app.config.settings import Settings
import asyncio

settings = Settings()

class Retrieve:
    def __init__(self):
        self.embedding = embedding
        self.chat = chat
        #search query
        """
        get email -> document
        
        store into DB (Database) 

        equivalent version of ChromaDB .query -> gert context
        """

    async def query(self, query:str)->List[float]:
        return await self.embedding.embed_query(query)

    async def get_context(self, query: str, top_k:int = 5):
        embedded_query:List[float] = await self.query(query)
        results = db.vector_search(embedded_query, top_k)
        return results

    async def answer(self, query:str):
        context = await self.get_context(query)
        answer = ""
        async for token in self.chat.generate_answer(query, context):
            answer += token
        return answer

retrieve = Retrieve()

if __name__ == "__main__":
    query = "Is there any security mail ?"
    result = asyncio.run(retrieve.answer(query))
    print(result)