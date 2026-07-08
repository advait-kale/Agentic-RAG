from chunking import chunker
from embeddings import embedding
from chat import chat

class Retrieve:
    def __init__(self):
        self.chunker = chunker
        self.embedding = embedding
        self.chat = chat
        self._get_embeddedquery()
        #search query
        """
        get email -> document
        
        store into DB (Database) 

        equivalent version of ChromaDB .query -> gert context
        """

    def _get_embeddedquery(self, query: str):
        return self.embedding.embed_query(query)

    def search(self):
        continue 

    def get_context(self, query: str):
        em_query = self._get_embeddedquery(query)
        


