#FASTAPI Backend
from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="Agentic RAG", description="This fetches the mail onto the RAG database sorts the SPAM and the SCAM Understands the IMP mail and links." )

