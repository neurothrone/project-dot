from enum import Enum
from os import getenv, urandom
from pathlib import Path

from pydantic import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


class Settings(BaseSettings):
    # SECRET_KEY: str
    # DEBUG: bool = False
    PROJECT_TITLE: str = "Developers of Teknikhögskolan"
    PROJECT_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "testing"

    # Database
    DB_URL: str | None = None

    # Search
    USERS_PER_PAGE: int = 6
    PROJECTS_PER_PAGE: int = 6

    class Config:
        env_file = ".env"
        case_sensitive = True

    def get_db_url(self, config_type: ConfigType | None = None) -> str:
        if self.DB_URL:
            return self.DB_URL

        if not config_type:
            config_type = ConfigType(self.ENVIRONMENT)

        match config_type:
            case ConfigType.DEVELOPMENT:
                return "sqlite:///data-dev.db"
            case ConfigType.TESTING:
                return "sqlite:///:memory:"
            case _:
                return "sqlite:///data.db"


settings = Settings()


class Config:
    SECRET_KEY = getenv("SECRET_KEY") or urandom(24)

    # Mail setup
    MAIL_SERVER = getenv("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = int(getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = getenv("MAIL_USE_TLS", "true").lower() in ["true", "on", "1"]
    MAIL_USERNAME = getenv("MAIL_USERNAME")
    MAIL_PASSWORD = getenv("MAIL_PASSWORD")
    DOT_MAIL_SUBJECT_PREFIX = "[DoT]"
    DOT_MAIL_SENDER = 'DoT Admin <dot@example.com>'

    # Permission
    DOT_ADMIN_EMAIL = getenv("DOT_ADMIN_EMAIL")
    # DOT_ADMIN_EMAILS: list[str] = getenv("DOT_ADMIN_EMAILS").split(",")

    # Files
    MAX_CONTENT_LENGTH = 1024 ** 2
    ALLOWED_UPLOAD_EXTENSIONS = [".jpg", ".png", ".gif"]
    UPLOAD_PATH_PROFILES = BASE_DIR / "app/static/img/uploads/profiles"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False


__configs = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(config_type: ConfigType) -> Config:
    return __configs.get(config_type.value, DevelopmentConfig)
