import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import Config

class Email_service:
    def __init__(self, to_email: str, subject: str, plain_text: str, from_email: str = None, from_field_name: str = None):
        self.to = to_email
        self.from_email = from_email or Config.MAIL_DEFAULT_SENDER
        self.from_name = from_field_name or Config.MAIL_DEFAULT_SENDER_NAME
        self.subject = subject
        self.body = plain_text
        self.MIME = MIMEMultipart("alternative")
        self.MIME['Subject'] = subject
        self.MIME['To'] = to_email
        self.MIME['From'] = f"{self.from_name} <{self.from_email}>"
        self.MIME.attach(MIMEText(plain_text, "plain"))
    
    def send(self):   
        try:
            server = smtplib.SMTP(Config.MAIL_SERVER, Config.MAIL_PORT)
            server.starttls()
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.sendmail(self.from_email, self.to, self.MIME.as_string())
            server.quit()
            return "OK"
        except Exception as error:
            return str(error)