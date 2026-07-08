from collections import defaultdict
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uuid

class Chunking:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, raw_docs):   # raw_docs: [{"source":..., "text":...}]
        docs = [Document(page_content=d["text"], metadata={"source": d["source"]})
                for d in raw_docs]
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""],
        )
        splits = splitter.split_documents(docs)

        counters = defaultdict(int)
        chunks = []
        for s in splits:
            src = s.metadata["source"]
            i = counters[src]
            counters[src] += 1
            chunks.append({
                "chunk_id": f"{uuid.uuid4().hex[:8]}_{i}",
                "source": src,
                "text": s.page_content,
            })
        return chunks

chunker = Chunking()