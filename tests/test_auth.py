"""Authentication functional tests using Page Object Model."""
import pytest
from playwright.sync_api import Page
from pages import LoginPage, DashboardPage
from config import TestData


@pytest.mark.auth
@pytest.mark.smoke
class TestLogin:
    """Test login functionality."""

    def test_login_page_loads(self, page: Page):
        """Test that login page loads successfully."""
        login_page = LoginPage(page)
        login_page.navigate()

        # Verify login form elements exist
        login_page.expect_login_page_loaded()

    def test_successful_login(self, page: Page):
        """Test successful login with valid credentials."""
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)

        login_page.navigate()
        login_page.login(TestData.PRIMARY_USER)

        # Should redirect to dashboard
        dashboard_page.expect_logged_in()

    def test_login_with_invalid_email(self, page: Page):
        """Test login fails with invalid email."""
        login_page = LoginPage(page)

        login_page.navigate()
        login_page.login_with_credentials('invalid@example.com', 'password123', wait_for_redirect=False)

        # Should show error message
        login_page.expect_error_message()

        # Should remain on login page
        login_page.expect_on_login_page()

    def test_login_with_invalid_password(self, page: Page):
        """Test login fails with invalid password."""
        login_page = LoginPage(page)

        login_page.navigate()
        login_page.login_with_credentials(
            TestData.PRIMARY_USER.email,
            'wrongpassword',
            wait_for_redirect=False
        )

        # Should show error message
        login_page.expect_error_message()

        # Should remain on login page
        login_page.expect_on_login_page()

    def test_login_with_empty_fields(self, page: Page):
        """Test login validation with empty fields."""
        login_page = LoginPage(page)

        login_page.navigate()

        # Try to submit without filling fields
        login_page.click_submit()

        # HTML5 validation should prevent submission
        # Check if still on login page
        login_page.expect_on_login_page()

    def test_login_multiple_users(self, page: Page):
        """Test login works for different users."""
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)

        for user in TestData.get_all_users():
            login_page.navigate()
            login_page.login(user)

            # Should redirect to dashboard
            dashboard_page.expect_logged_in()

            # Logout
            dashboard_page.logout()


@pytest.mark.auth
class TestLogout:
    """Test logout functionality."""

    def test_logout_successful(self, authenticated_page: Page):
        """Test user can logout successfully."""
        dashboard_page = DashboardPage(authenticated_page)
        login_page = LoginPage(authenticated_page)

        # Verify we're logged in
        dashboard_page.expect_logged_in()

        # Click logout
        dashboard_page.logout()

        # Try to access dashboard
        dashboard_page.navigate()

        # Should redirect back to login
        login_page.expect_on_login_page()

    def test_logout_clears_session(self, authenticated_page: Page):
        """Test logout clears user session."""
        dashboard_page = DashboardPage(authenticated_page)

        # Logout
        dashboard_page.logout()

        # Check localStorage is cleared
        token = dashboard_page.get_local_storage_item("token")
        user = dashboard_page.get_local_storage_item("user")

        assert token is None, "Token should be cleared from localStorage"
        assert user is None, "User should be cleared from localStorage"


@pytest.mark.auth
class TestRegister:
    """Test registration functionality."""

    def test_register_page_loads(self, page: Page):
        """Test register page loads successfully."""
        login_page = LoginPage(page)
        login_page.goto(login_page.settings.register_url)
        login_page.wait_for_url('/register')

        # Verify registration form elements
        login_page.expect_visible('input[name="name"]')
        login_page.expect_visible('input[type="email"]')
        login_page.expect_visible('input[type="password"]')
        login_page.expect_visible('button[type="submit"]')

    def test_navigate_between_login_and_register(self, page: Page):
        """Test navigation between login and register pages."""
        login_page = LoginPage(page)

        login_page.navigate()

        # Click link to register page
        login_page.navigate_to_register()

        # Click link to login page
        login_page.click(login_page.LOGIN_LINK)

        # Should navigate to login page
        login_page.expect_on_login_page()


@pytest.mark.auth
class TestProtectedRoutes:
    """Test protected route access."""

    def test_unauthenticated_access_to_dashboard(self, page: Page):
        """Test unauthenticated user cannot access dashboard."""
        dashboard_page = DashboardPage(page)
        login_page = LoginPage(page)

        dashboard_page.navigate()

        # Should redirect to login
        login_page.expect_on_login_page()

    def test_unauthenticated_access_to_trading(self, page: Page):
        """Test unauthenticated user cannot access trading page."""
        login_page = LoginPage(page)

        page.goto(login_page.settings.trading_url)

        # Should redirect to login
        login_page.expect_on_login_page()

    def test_unauthenticated_access_to_portfolio(self, page: Page):
        """Test unauthenticated user cannot access portfolio page."""
        login_page = LoginPage(page)

        page.goto(login_page.settings.portfolio_url)

        # Should redirect to login
        login_page.expect_on_login_page()

    def test_unauthenticated_access_to_watchlists(self, page: Page):
        """Test unauthenticated user cannot access watchlists page."""
        login_page = LoginPage(page)

        page.goto(login_page.settings.watchlists_url)

        # Should redirect to login
        login_page.expect_on_login_page()

    def test_unauthenticated_access_to_trades(self, page: Page):
        """Test unauthenticated user cannot access trades page."""
        login_page = LoginPage(page)

        page.goto(login_page.settings.trades_url)

        # Should redirect to login
        login_page.expect_on_login_page()

    def test_authenticated_access_to_all_pages(self, authenticated_page: Page):
        """Test authenticated user can access all protected pages."""
        login_page = LoginPage(authenticated_page)

        pages_to_test = [
            login_page.settings.dashboard_url,
            login_page.settings.trading_url,
            login_page.settings.portfolio_url,
            login_page.settings.trades_url,
            login_page.settings.watchlists_url
        ]

        for route in pages_to_test:
            authenticated_page.goto(route)
            authenticated_page.wait_for_url(route)
            # Should not redirect to login
            assert '/login' not in authenticated_page.url
