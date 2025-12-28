"""Pytest configuration and fixtures using OOP architecture."""
import pytest
from playwright.sync_api import Page, BrowserContext
from config import settings, TestData
from pages import LoginPage, DashboardPage


@pytest.fixture(scope='session')
def browser_context_args(browser_context_args):
    """Configure browser context arguments using settings."""
    return {
        **browser_context_args,
        'viewport': {
            'width': settings.viewport_width,
            'height': settings.viewport_height
        },
        'base_url': settings.base_url,
    }


@pytest.fixture(scope='session')
def browser_type_launch_args(browser_type_launch_args):
    """Configure browser launch arguments using settings."""
    return {
        **browser_type_launch_args,
        'headless': settings.headless,
        'slow_mo': settings.slow_mo,
    }


@pytest.fixture
def page(page: Page):
    """Configure page with default timeout from settings."""
    page.set_default_timeout(settings.timeout)
    yield page


@pytest.fixture
def authenticated_page(page: Page):
    """Fixture that provides an authenticated page with logged-in user.

    Uses Page Object Model for authentication.
    """
    login_page = LoginPage(page)
    dashboard_page = DashboardPage(page)

    # Navigate to base URL
    page.goto(settings.base_url)

    # Check if we're redirected to login page, if so perform login
    if '/login' in page.url:
        # Perform login using Page Object
        login_page.login(TestData.PRIMARY_USER, wait_for_redirect=True)

    yield page

    # Cleanup: logout after test
    try:
        dashboard_page.logout()
    except:
        pass  # Already logged out or page closed


@pytest.fixture(autouse=True)
def clear_storage(context: BrowserContext):
    """Clear browser storage before each test."""
    context.clear_cookies()
    yield
