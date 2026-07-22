#FASTAPI Backend
from fastapi import FastAPI, File, UploadFile
from app.services.RAG import retrieve
from sql.database import db
import asyncio

app = FastAPI(title="Agentic RAG", description="This fetches the mail onto the RAG database sorts the SPAM and Understands the IMP mail and links." )

@app.on_event("startup")
async def startup_event():
    db.connect()

@app.post("/query")
async def query(query: str):
    return await retrieve.answer(query)
