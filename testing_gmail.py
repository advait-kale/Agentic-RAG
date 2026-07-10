from simplegmail import Gmail
from simplegmail.query import construct_query
from bs4 import BeautifulSoup
from rich.console import Console
from rich.pretty import Pretty
from rich.panel import Panel
import re

console = Console()

gmail = Gmail()

def clean_body(m):
    raw = m.plain or m.html or ""
    if "<" in raw and ">" in raw:            # html → text
        raw = BeautifulSoup(raw, "html.parser").get_text(" ")
    raw = re.sub(r"https?://\S+", "", raw)   # kill tracking urls
    raw = re.sub(r"[\u200b-\u200f\ufeff\u00ad]", "", raw)  # zero-width junk
    raw = re.sub(r"\s+", " ", raw).strip()   # collapse whitespace
    return raw

 # -> testing
query_params_1 = {
    "newer_than": (2, "day")
}

messages = gmail.get_messages(query=construct_query(query_params_1))

console.print(Panel(Pretty(messages)))

for m in messages:
    console.print(Panel(Pretty(
        f"Sender {m.sender}\n"
        f"Recipient {m.recipient}\n"
        f"Subject {m.subject}"
        # f"Sbippet{m.snippet.encode('ascii', 'ignore').decode()}\n"
        f"m.html {clean_body(m)}"
    )))
