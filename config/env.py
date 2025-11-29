from dataclasses import dataclass
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent


def _load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    for line in env_path.read_text().splitlines():
        if not line or line.strip().startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_env_file(BASE_DIR / ".env")


def _env_bool(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() in {"1", "true", "yes"}


@dataclass
class DjangoSettings:
    secret_key: str = os.getenv("DJANGO_SECRET_KEY", "dev-secret-key")
    debug: bool = _env_bool("DEBUG", True)
    allowed_hosts: list[str] = None

    def __post_init__(self) -> None:
        self.allowed_hosts = os.getenv("ALLOWED_HOSTS", "*").split(",")


@dataclass
class DatabaseSettings:
    url: str = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")


@dataclass
class WahaSettings:
    base_url: str = os.getenv("WAHA_URL", "http://localhost:3000")
    api_key: str = os.getenv("WAHA_API_KEY", "dev-api-key")
    session_name: str = os.getenv("WAHA_SESSION_NAME", "dev-session")
    timeout_seconds: int = int(os.getenv("WAHA_TIMEOUT_SECONDS", "5"))


@dataclass
class BotDashboardCredentials:
    username: str = os.getenv("BOT_DASHBOARD_USERNAME", "admin")
    password: str = os.getenv("BOT_DASHBOARD_PASSWORD", "password")


@dataclass
class DjangoAdminCredentials:
    username: str = os.getenv("DJANGO_ADMIN_USERNAME", "admin")
    password: str = os.getenv("DJANGO_ADMIN_PASSWORD", "admin")


@dataclass
class AppConfig:
    django: DjangoSettings = None
    database: DatabaseSettings = None
    waha: WahaSettings = None
    dashboard_credentials: BotDashboardCredentials = None
    admin_credentials: DjangoAdminCredentials = None

    def __post_init__(self) -> None:
        self.django = DjangoSettings()
        self.database = DatabaseSettings()
        self.waha = WahaSettings()
        self.dashboard_credentials = BotDashboardCredentials()
        self.admin_credentials = DjangoAdminCredentials()


settings = AppConfig()
