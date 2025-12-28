"""User model for test framework."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """User model representing a test user."""

    email: str
    password: str
    name: str
    token: Optional[str] = None

    def __post_init__(self):
        """Validate user data after initialization."""
        if not self.email:
            raise ValueError("Email cannot be empty")
        if not self.password:
            raise ValueError("Password cannot be empty")
        # Name is optional for some test scenarios

    def to_dict(self) -> dict:
        """Convert user to dictionary.

        Returns:
            Dictionary representation of user
        """
        return {
            'email': self.email,
            'password': self.password,
            'name': self.name
        }

    def __repr__(self) -> str:
        """String representation of user (hides password)."""
        return f"User(email='{self.email}', name='{self.name}')"
