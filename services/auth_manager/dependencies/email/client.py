from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from threading import Lock
from typing import Optional, Dict
from dataclasses import dataclass
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from .config import Settings

@dataclass
class Email:
    _instance: Optional["Email"] = None
    _lock: Lock = Lock()
    conf = None
    jinja_env = None

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.settings = Settings()
        self.conf: ConnectionConfig = ConnectionConfig(
            MAIL_USERNAME=self.settings.smtp_user,
            MAIL_PASSWORD=self.settings.smtp_pass,
            MAIL_FROM=self.settings.smtp_default_from_address,
            MAIL_PORT=self.settings.smtp_port,
            MAIL_SERVER=self.settings.smtp_host,
            MAIL_FROM_NAME=self.settings.mail_from_name,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=False,
            TEMPLATE_FOLDER=self.settings.template_folder_path,
        )
        
        template_path = Path(self.settings.template_folder_path)
        if template_path.exists():
            self.jinja_env = Environment(
                loader=FileSystemLoader(str(template_path)),
                autoescape=True
            )

    def _render_template(self, template_name: str, context: Dict) -> str:
        if not self.jinja_env:
            raise ValueError(f"Template folder not found: {self.settings.template_folder_path}")
        
        try:
            template = self.jinja_env.get_template(template_name)
            return template.render(**context)
        except Exception as e:
            raise ValueError(f"Error rendering template {template_name}: {str(e)}")

    async def send_email(
        self,
        to: list[str],
        subject: str,
        template_name: Optional[str] = None,
        context: Optional[Dict] = None,
        body: Optional[str] = None,
        sender: Optional[str] = None
    ):
        sender = sender or self.settings.smtp_user
        
        if template_name and context:
            body = self._render_template(template_name, context)
            subtype = "html"
        elif template_name:
            body = self._render_template(template_name, {})
            subtype = "html"
        else:
            body = body if body else ""
            subtype = "html" if "<" in body else "plain"
        
        message = MessageSchema(
            subject=subject,
            recipients=to,
            body=body,
            subtype=subtype,
        )
        
        fm = FastMail(self.conf)
        await fm.send_message(message)

def get_email() -> Email:
    return Email()