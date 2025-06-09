from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    smtp_host: str = "mailhog"
    smtp_port: int = 1025
    smtp_user: str
    smtp_pass: str
    mail_from_name: str = "Urban Hotel"
    smtp_default_from_address: str = "noreply@urbanhotel.com"
    template_folder: str = "templates"

    @property
    def template_folder_path(self) -> str:
        base_dir = Path(__file__).parent.parent.parent
        folder = base_dir / self.template_folder
        return str(folder.resolve())