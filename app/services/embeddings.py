from langchain_ollama import OllamaEmbeddings

embedding_model = "qwen3-embedding:0.6b"

class Embedding:
    def __init__(self):
        self.embedding_model = OllamaEmbeddings(model=embedding_model)
    
    async def embed_documents(self, texts):
        return self.embedding_model.embed_documents(texts)
    
    async  def embed_query(self, text):
        return self.embedding_model.embed_query(text)
    
embedding = Embedding()