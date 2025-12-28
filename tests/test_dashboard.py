"""Dashboard page functional tests using Page Object Model."""
import pytest
from playwright.sync_api import Page
from pages import DashboardPage


@pytest.mark.dashboard
@pytest.mark.smoke
class TestDashboardLoad:
    """Test dashboard page loading."""

    def test_dashboard_page_loads(self, authenticated_page: Page):
        """Test dashboard page loads successfully."""
        dashboard_page = DashboardPage(authenticated_page)
        dashboard_page.navigate()

        # Verify dashboard is loaded
        dashboard_page.expect_dashboard_loaded()

    def test_portfolio_summary_displayed(self, authenticated_page: Page):
        """Test portfolio summary is displayed."""
        dashboard_page = DashboardPage(authenticated_page)
        dashboard_page.navigate()

        # Check portfolio summary is visible
        dashboard_page.expect_portfolio_summary_visible()

    def test_navigation_visible(self, authenticated_page: Page):
        """Test navigation menu is visible."""
        dashboard_page = DashboardPage(authenticated_page)
        dashboard_page.navigate()

        # Check navigation is visible
        dashboard_page.expect_navigation_visible()


@pytest.mark.dashboard
class TestDashboardMetrics:
    """Test dashboard metrics display."""

    def test_portfolio_value_displayed(self, authenticated_page: Page):
        """Test portfolio value is displayed."""
        dashboard_page = DashboardPage(authenticated_page)
        dashboard_page.navigate()

        # Portfolio value should be visible
        assert dashboard_page.is_portfolio_summary_displayed(), "Portfolio summary should be displayed"

    def test_cash_balance_displayed(self, authenticated_page: Page):
        """Test cash balance is displayed."""
        dashboard_page = DashboardPage(authenticated_page)
        dashboard_page.navigate()

        # Cash balance should be visible
        assert dashboard_page.is_portfolio_summary_displayed(), "Cash balance should be displayed"


@pytest.mark.dashboard
class TestDashboardNavigation:
    """Test dashboard navigation."""

    def test_navigate_to_trading(self, authenticated_page: Page):
        """Test navigation to trading page."""
        dashboard_page = DashboardPage(authenticated_page)
        dashboard_page.navigate()

        # Navigate to trading
        dashboard_page.navigate_to_trading()

        # Verify URL
        dashboard_page.expect_url('/trading')

    def test_navigate_to_portfolio(self, authenticated_page: Page):
        """Test navigation to portfolio page."""
        dashboard_page = DashboardPage(authenticated_page)
        dashboard_page.navigate()

        # Navigate to portfolio
        dashboard_page.navigate_to_portfolio()

        # Verify URL
        dashboard_page.expect_url('/portfolio')

    def test_navigate_to_watchlists(self, authenticated_page: Page):
        """Test navigation to watchlists page."""
        dashboard_page = DashboardPage(authenticated_page)
        dashboard_page.navigate()

        # Navigate to watchlists
        dashboard_page.navigate_to_watchlists()

        # Verify URL
        dashboard_page.expect_url('/watchlists')

    def test_navigate_to_trades(self, authenticated_page: Page):
        """Test navigation to trade history page."""
        dashboard_page = DashboardPage(authenticated_page)
        dashboard_page.navigate()

        # Navigate to trades
        dashboard_page.navigate_to_trades()

        # Verify URL
        dashboard_page.expect_url('/trades')
