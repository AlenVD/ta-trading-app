"""Centralized configuration management for test framework."""
import os
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv


@dataclass
class Settings:
    """Test framework settings loaded from environment variables."""

    # URLs
    base_url: str
    api_url: str

    # Browser settings
    headless: bool
    slow_mo: int
    timeout: int

    # Viewport settings
    viewport_width: int
    viewport_height: int

    # Report settings
    report_dir: str
    screenshot_dir: str

    @classmethod
    def from_env(cls, env_file: str = '.env.test') -> 'Settings':
        """Load settings from environment file.

        Args:
            env_file: Path to environment file

        Returns:
            Settings instance with loaded values
        """
        load_dotenv(env_file)

        return cls(
            base_url=os.getenv('BASE_URL', 'http://localhost:5173'),
            api_url=os.getenv('API_URL', 'http://localhost:5001/api'),
            headless=os.getenv('HEADLESS', 'true').lower() == 'false',
            slow_mo=int(os.getenv('SLOW_MO', '0')),
            timeout=int(os.getenv('TIMEOUT', '30000')),
            viewport_width=int(os.getenv('VIEWPORT_WIDTH', '1920')),
            viewport_height=int(os.getenv('VIEWPORT_HEIGHT', '1080')),
            report_dir=os.getenv('REPORT_DIR', 'reports'),
            screenshot_dir=os.getenv('SCREENSHOT_DIR', 'reports/screenshots')
        )

    @property
    def login_url(self) -> str:
        """Get login page URL."""
        return f"{self.base_url}/login"

    @property
    def dashboard_url(self) -> str:
        """Get dashboard page URL."""
        return f"{self.base_url}/dashboard"

    @property
    def trading_url(self) -> str:
        """Get trading page URL."""
        return f"{self.base_url}/trading"

    @property
    def portfolio_url(self) -> str:
        """Get portfolio page URL."""
        return f"{self.base_url}/portfolio"

    @property
    def watchlists_url(self) -> str:
        """Get watchlists page URL."""
        return f"{self.base_url}/watchlists"

    @property
    def trades_url(self) -> str:
        """Get trade history page URL."""
        return f"{self.base_url}/trades"

    @property
    def register_url(self) -> str:
        """Get registration page URL."""
        return f"{self.base_url}/register"


# Global settings instance
settings = Settings.from_env()
