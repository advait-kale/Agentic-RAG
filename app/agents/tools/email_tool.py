#uv run -m app.agents.tools.email_tool

from GmailAPI import gmailAPI
from rich.console import Console
from rich.pretty import Pretty
from rich.panel import Panel

console = Console()

console.print(Panel(Pretty(gmailAPI.mail_body())))