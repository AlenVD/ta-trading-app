"""Test data management for test framework."""
from typing import List
from models.user import User


class TestData:
    """Centralized test data management."""

    # Test users
    PRIMARY_USER = User(
        email='john@example.com',
        password='password123',
        name='John Doe'
    )

    SECONDARY_USER = User(
        email='jane@example.com',
        password='password123',
        name='Jane Smith'
    )

    TERTIARY_USER = User(
        email='bob@example.com',
        password='password123',
        name='Bob Johnson'
    )

    @classmethod
    def get_all_users(cls) -> List[User]:
        """Get all test users.

        Returns:
            List of all test users
        """
        return [cls.PRIMARY_USER, cls.SECONDARY_USER, cls.TERTIARY_USER]

    @classmethod
    def get_invalid_user(cls) -> User:
        """Get invalid user credentials for negative testing.

        Returns:
            User with invalid credentials
        """
        return User(
            email='invalid@example.com',
            password='wrongpassword',
            name='Invalid User'
        )

    # Stock symbols for testing
    STOCK_SYMBOLS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA', 'NVDA', 'AMZN', 'META']

    # Trade amounts for testing
    DEFAULT_TRADE_QUANTITY = 10
    LARGE_TRADE_QUANTITY = 100
    SMALL_TRADE_QUANTITY = 1
