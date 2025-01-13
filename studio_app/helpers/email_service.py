import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ..config import Config

class Email_helper():
    pass

def send_email(to_email: str, subject: str, plain_text, from_email: str = None, from_field_name = ""):
    config = Config()

    message = MIMEMultipart("alternative")
    message['Subject'] = subject
    message['To'] = to_email
    message['From'] = f"{from_field_name} <{config.MAIL_DEFAULT_SENDER if from_email is None else from_email}>"
    message.attach(MIMEText(plain_text, "plain"))

    try:
        server = smtplib.SMTP(config.MAIL_SERVER, config.MAIL_PORT)
        server.starttls()
        server.login(config.MAIL_USERNAME, config.MAIL_PASSWORD)
        server.sendmail(from_email, to_email, message.as_string())
        server.quit()
        return "OK"
    except Exception as error:
        return str(error)