from simplegmail import Gmail
from simplegmail.query import construct_query
from bs4 import BeautifulSoup
import re
from typing import List, Dict

class GmailAPI:
    def __init__(self):
        self.gmail = None

    def client(self):
        if self.gmail is None:
            self.gmail = Gmail()
        return self.gmail

    def clean_body(self, m):
        raw = m.plain or m.html or ""
        if "<" in raw and ">" in raw:            # html → text
            raw = BeautifulSoup(raw, "html.parser").get_text(" ")
        raw = re.sub(r"https?://\S+", "", raw)   # kill tracking urls
        raw = re.sub(r"[\u200b-\u200f\ufeff\u00ad]", "", raw)  # zero-width junk
        raw = re.sub(r"\s+", " ", raw).strip()   # collapse whitespace
        return raw

    def mail_body(self) -> List[dict]:
        # -> testing
        query_params_1 = {
            "newer_than": (2, "day")
        }

        messages = self.client().get_messages(query=construct_query(query_params_1))

        return [
            {
                "id": m.id,
                "thread_id": m.thread_id,
                "date": m.date,
                "sender": m.sender,
                "recipient": m.recipient,
                "subject": m.subject,
                "body": self.clean_body(m)
            }
            for m in messages
        ]        

gmailAPI = GmailAPI() # global call