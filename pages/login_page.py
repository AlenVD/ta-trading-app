"""Login page object."""
from typing import Optional
from playwright.sync_api import Page
from .base_page import BasePage
from models.user import User


class LoginPage(BasePage):
    """Login page object with login-specific functionality."""

    # Locators as class constants
    EMAIL_INPUT = 'input[type="email"]'
    PASSWORD_INPUT = 'input[type="password"]'
    SUBMIT_BUTTON = 'button[type="submit"]'
    ERROR_MESSAGE = 'text=/invalid credentials|user not found|invalid password/i'
    REGISTER_LINK = 'text=/sign up|register|create account/i'
    LOGIN_LINK = 'text=/sign in|login|already have/i'

    def __init__(self, page: Page):
        """Initialize login page.

        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = self.settings.login_url

    def navigate(self):
        """Navigate to login page."""
        self.goto(self.url)
        self.wait_for_url('/login')

    def is_loaded(self) -> bool:
        """Check if login page is fully loaded.

        Returns:
            True if page is loaded, False otherwise
        """
        return (
            self.is_visible(self.EMAIL_INPUT) and
            self.is_visible(self.PASSWORD_INPUT) and
            self.is_visible(self.SUBMIT_BUTTON)
        )

    def fill_email(self, email: str):
        """Fill email input field.

        Args:
            email: Email address
        """
        self.fill(self.EMAIL_INPUT, email)

    def fill_password(self, password: str):
        """Fill password input field.

        Args:
            password: Password
        """
        self.fill(self.PASSWORD_INPUT, password)

    def click_submit(self):
        """Click submit button."""
        self.click(self.SUBMIT_BUTTON)

    def login(self, user: User, wait_for_redirect: bool = True):
        """Perform login with user credentials.

        Args:
            user: User object with email and password
            wait_for_redirect: Whether to wait for redirect to dashboard
        """
        self.fill_email(user.email)
        self.fill_password(user.password)
        self.click_submit()

        if wait_for_redirect:
            self.wait_for_url('/dashboard', timeout=self.timeout)

    def login_with_credentials(self, email: str, password: str, wait_for_redirect: bool = True):
        """Perform login with email and password.

        Args:
            email: Email address
            password: Password
            wait_for_redirect: Whether to wait for redirect to dashboard
        """
        user = User(email=email, password=password, name='')
        self.login(user, wait_for_redirect)

    def is_error_displayed(self) -> bool:
        """Check if error message is displayed.

        Returns:
            True if error is visible, False otherwise
        """
        return self.is_visible(self.ERROR_MESSAGE)

    def get_error_message(self) -> Optional[str]:
        """Get error message text.

        Returns:
            Error message text or None
        """
        if self.is_error_displayed():
            return self.get_text(self.ERROR_MESSAGE)
        return None

    def navigate_to_register(self):
        """Navigate to register page."""
        self.click(self.REGISTER_LINK)
        self.wait_for_url('/register')

    def is_on_login_page(self) -> bool:
        """Check if currently on login page.

        Returns:
            True if on login page, False otherwise
        """
        return '/login' in self.get_current_url()

    # Validation methods
    def expect_login_page_loaded(self):
        """Assert that login page is loaded."""
        self.expect_visible(self.EMAIL_INPUT)
        self.expect_visible(self.PASSWORD_INPUT)
        self.expect_visible(self.SUBMIT_BUTTON)

    def expect_error_message(self):
        """Assert that error message is displayed."""
        self.expect_visible(self.ERROR_MESSAGE, timeout=5000)

    def expect_on_login_page(self):
        """Assert that we are on login page."""
        self.expect_url('/login')
