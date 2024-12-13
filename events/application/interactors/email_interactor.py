import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from events.application.interfaces.email_interface import EmailSender


class SMTPEmailSender(EmailSender):
    def __init__(self, smtp_server: str, smtp_port: int, login: str, password: str) -> None:
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port
        self._login = login
        self._password = password

    async def send_email(self, recipient: str, subject: str, body: str) -> None:
        msg = MIMEMultipart()
        msg['From'] = self._login
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            with smtplib.SMTP(self._smtp_server, self._smtp_port) as server:
                server.starttls()
                server.login(self._login, self._password)
                server.send_message(msg)
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}")
