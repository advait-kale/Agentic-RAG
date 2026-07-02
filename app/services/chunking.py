from langchain_text_splitters import RecursiveCharacterTextSplitter

class Chunking:
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, documents):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = self.chunk_size,
            chunk_overlap = self.chunk_overlap,
            separators=["\n\n", "\n", ".", " ", ""]
        )
        return splitter.split_documents(documents) # document is a list of langchain documents

chunker = Chunking()