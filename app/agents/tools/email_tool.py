#uv run -m app.agents.tools.email_tool

import asyncio

from GmailAPI import gmailAPI

from langchain_core.documents import Document

from sql.database import db
from app.services.chunking import chunker
from app.services.embeddings import embedding


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
    
    db.connect()
    db.upsert_chunks(chunked_mail)

if __name__ == "__main__":
    asyncio.run(seed_mail())


        
