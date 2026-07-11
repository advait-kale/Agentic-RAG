#FASTAPI Backend
from fastapi import FastAPI, File, UploadFile

app = FastAPI(title="Agentic RAG", description="This fetches the mail onto the RAG database sorts the SPAM and Understands the IMP mail and links." )

@app.on_event("startup")
async def startup_event():
    continue
