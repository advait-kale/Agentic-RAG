import imaplib
import email
from email import policy
from email.parser import BytesParser
from datetime import datetime, timedelta
from config.settings import Settings

settings = Settings()

class Email:
    def __init__(self):
        self.username  = settings.email_address
        self.password  = settings.app_password
        self._connect_Google_acc()

    def _connect_Google_acc(self):

        try:
            imap = imaplib.IMAP4_SSL("imap.gmail.com")
            imap.login(self.username, self.password) 
            

            imap.select("INBOX") 
            status, data = imap.search(None, 'ALL')

            email_ids = data[0].split()

            messages = []
            for eid in email_ids:
                status, msg_data = imap.fetch(eid, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                messages.append(msg)
            imap.logout()
        except Exception as e:
            print(f"Error in Google connect {e}")