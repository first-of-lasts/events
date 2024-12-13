import aiosmtplib
from email.message import EmailMessage

from events.application.interfaces.email_interface import EmailSender


class EmailGateway(EmailSender):
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self._smtp_server = smtp_server
        self._smtp_port = smtp_port
        self._username = username
        self._password = password

    async def send_email(self, recipient: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self._username
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)
        try:
            await aiosmtplib.send(
                message,
                hostname=self._smtp_server,
                port=self._smtp_port,
                username=self._username,
                password=self._password,
                use_tls=True,
            )
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {e}")


class MockEmailGateway(EmailSender):
    async def send_email(self, recipient: str, subject: str, body: str) -> None:
        print(f"Mock email sent to {recipient} with subject '{subject}' and body:\n{body}")
