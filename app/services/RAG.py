from chunking import chunker
from embeddings import embedding
from chat import chat
from sql.database import db
import asyncio

class Retrieve:
    def __init__(self):
        self.chunker = chunker
        self.embedding = embedding
        self.chat = chat
        #search query
        """
        get email -> document
        
        store into DB (Database) 

        equivalent version of ChromaDB .query -> gert context
        """

    def get_context(self, query: str):
        em_query = self.get_embeddedquery(query)

    async def semantic_search(self, query: str, top_k:int = 5, min_similarity:float = 0.0):
        embed_query = await self.embedding.embed_query(query)
        results = await db.vector_search(embed_query, top_k, min_similarity)
        return results
    
    def answer(self, query:str):
        db.connect()                                                                                                                  
        for r in asyncio.run(semantic_search(query)):                                                         
            print(f'{r["source"]} ({r["similarity"] * 100:.1f}% similar)')                                                            
        
