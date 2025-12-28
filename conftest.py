"""Pytest configuration and fixtures using OOP architecture.

This file has been extended to support session-auth for tests marked with the
`trading` marker. When trading tests are present in the test session we create
and reuse a Playwright storage state file so the application is logged in once
and available to tests that require authentication.
"""
import pytest
from typing import Optional
from playwright.sync_api import Page, BrowserContext
from config import settings, TestData
from pages import LoginPage, DashboardPage

#TODO: make wait for visible default based on config settings -> also config based on env
#TODO: add reportportal logging
#TODO: add screenshot on failure
#TODO: parse non pythonic test case names in reports


def pytest_collection_modifyitems(config, items):
    # Check if there are tests that are NOT marked with 'login'
    # This implies we have functional tests that need a session
    config.needs_login = any(not item.get_closest_marker("login") for item in items)


@pytest.fixture(scope='session')
def storage_state(tmp_path_factory, playwright, pytestconfig) -> Optional[str]:
    if not getattr(pytestconfig, 'needs_login', False):
        return None

    # Use a context manager for the browser to ensure it closes
    browser = playwright.chromium.launch(headless=settings.headless)
    
    try:
        context = browser.new_context(
            base_url=settings.base_url,
            viewport={'width': settings.viewport_width, 'height': settings.viewport_height}
        )
        page = context.new_page()
        page.goto("/")

        from pages.login_page import LoginPage
        login_page = LoginPage(page)
        
        # Add a timeout or check to ensure we actually need to log in
        login_page.login(TestData.PRIMARY_USER, wait_for_redirect=True)

        tmpdir = tmp_path_factory.mktemp("state")
        state_file = tmpdir / "storage_state.json"
        context.storage_state(path=str(state_file))
        return str(state_file)
    
    finally:
        browser.close()

@pytest.fixture(scope='session')
def browser_context_args(browser_context_args, storage_state: Optional[str]):
    """Configure browser context arguments using settings and optional storage state."""
    args = {
        **browser_context_args,
        'viewport': {
            'width': settings.viewport_width,
            'height': settings.viewport_height
        },
        'base_url': settings.base_url,
    }

    # If a storage state file was generated for the session, instruct Playwright
    # to initialize contexts with it. This makes pages authenticated from the
    # moment they are created.
    if storage_state:
        args['storage_state'] = storage_state

    return args


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
    except Exception:
        pass  # Already logged out or page closed


@pytest.fixture(autouse=True)
def clear_storage(context: BrowserContext, request):
    """Clear browser storage before each test unless the test is marked `trading`.

    Trading tests rely on session-authenticated storage state and therefore must
    not have their cookies/local storage cleared between tests; non-trading
    tests continue to get a clean context.
    """
    if request.node.get_closest_marker('trading') is None:
        # Only clear cookies for non-trading tests
        context.clear_cookies()
    yield
