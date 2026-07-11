#uv run -m app.agents.tools.email_tool

import asyncio

from GmailAPI import gmailAPI
from rich.console import Console
from rich.pretty import Pretty
from rich.panel import Panel

from langchain_core.documents import Document

from app.services.chunking import chunker
from app.services.embeddings import embedding

console = Console()

async def seed_mail():
    mail_record = gmailAPI.mail_body()
    if not mail_record:
        raise Exception("Error 400 : No mail found")
    print(f"number of mails {len(mail_record)}")

    raw_docs = [                                                              
        {                                                                     
            "source": f"email:{r['id']}",                                     
            "text": (                                                         
                f"From: {r['sender']} | To: {r['recipient']} | "              
                f"Subject: {r['subject']} | Date: {r['date']}\n\n{r['body']}" 
            ),                                                                
        }                                                                     
        for r in mail_record                                                      
    ]

    chunked_mail = chunker.chunk_text(raw_docs)

    embeded_chunks = await embedding.embed_mail([c["text"] for c in chunked_mail])

    for c, v in zip(chunked_mail, embeded_chunks):
        c["embedding"] = v
        
