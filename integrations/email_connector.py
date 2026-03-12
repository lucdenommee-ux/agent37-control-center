import imaplib
import email

class EmailConnector:

    def fetch(self, user, password):

        mail = imaplib.IMAP4_SSL("imap.gmail.com")
        mail.login(user, password)

        mail.select("inbox")

        status, data = mail.search(None, "ALL")

        return data

