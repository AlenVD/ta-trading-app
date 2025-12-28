"""Dashboard page object."""
from typing import Optional, Dict
from playwright.sync_api import Page
from .base_page import BasePage


class DashboardPage(BasePage):
    """Dashboard page object with dashboard-specific functionality."""

    # Locators
    DASHBOARD_HEADER = 'text=/dashboard/i'
    LOGOUT_BUTTON = 'text=Logout'
    PORTFOLIO_VALUE = 'text=/portfolio value|total value/i'
    CASH_BALANCE = 'text=/cash balance|available cash/i'
    PROFIT_LOSS = 'text=/profit|loss|p&l/i'
    TOP_POSITIONS = 'text=/top positions|holdings/i'
    NAVIGATION_MENU = 'nav'
    TRADING_LINK = 'text=/trading|trade stocks/i'
    PORTFOLIO_LINK = 'text=/portfolio/i'
    WATCHLISTS_LINK = 'text=/watchlist/i'
    TRADES_LINK = 'text=/trades|trade history/i'

    def __init__(self, page: Page):
        """Initialize dashboard page.

        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = self.settings.dashboard_url

    def navigate(self):
        """Navigate to dashboard page."""
        self.goto(self.url)
        self.wait_for_url('/dashboard')

    def is_loaded(self) -> bool:
        """Check if dashboard page is fully loaded.

        Returns:
            True if page is loaded, False otherwise
        """
        return (
            self.is_visible(self.DASHBOARD_HEADER) and
            self.is_visible(self.LOGOUT_BUTTON)
        )

    def logout(self):
        """Logout from application."""
        self.click(self.LOGOUT_BUTTON)
        self.wait_for_url('/login')

    def is_logged_in(self) -> bool:
        """Check if user is logged in.

        Returns:
            True if logged in, False otherwise
        """
        return self.is_visible(self.LOGOUT_BUTTON)

    # Navigation methods
    def navigate_to_trading(self):
        """Navigate to trading page."""
        self.click(self.TRADING_LINK)
        self.wait_for_url('/trading')

    def navigate_to_portfolio(self):
        """Navigate to portfolio page."""
        self.click(self.PORTFOLIO_LINK)
        self.wait_for_url('/portfolio')

    def navigate_to_watchlists(self):
        """Navigate to watchlists page."""
        self.click(self.WATCHLISTS_LINK)
        self.wait_for_url('/watchlists')

    def navigate_to_trades(self):
        """Navigate to trade history page."""
        self.click(self.TRADES_LINK)
        self.wait_for_url('/trades')

    # Portfolio metrics methods
    def is_portfolio_summary_displayed(self) -> bool:
        """Check if portfolio summary is displayed.

        Returns:
            True if portfolio summary is visible, False otherwise
        """
        return (
            self.is_visible(self.PORTFOLIO_VALUE) or
            self.is_visible(self.CASH_BALANCE)
        )

    def get_portfolio_value(self) -> Optional[float]:
        """Get portfolio value.

        Returns:
            Portfolio value or None
        """
        if self.is_visible(self.PORTFOLIO_VALUE):
            text = self.get_text(self.PORTFOLIO_VALUE)
            return self.extract_number_from_text(text) if text else None
        return None

    def get_cash_balance(self) -> Optional[float]:
        """Get cash balance.

        Returns:
            Cash balance or None
        """
        if self.is_visible(self.CASH_BALANCE):
            text = self.get_text(self.CASH_BALANCE)
            return self.extract_number_from_text(text) if text else None
        return None

    def is_top_positions_displayed(self) -> bool:
        """Check if top positions section is displayed.

        Returns:
            True if top positions is visible, False otherwise
        """
        return self.is_visible(self.TOP_POSITIONS)

    def is_navigation_visible(self) -> bool:
        """Check if navigation menu is visible.

        Returns:
            True if navigation is visible, False otherwise
        """
        return self.is_visible(self.NAVIGATION_MENU)

    # Validation methods
    def expect_dashboard_loaded(self):
        """Assert that dashboard page is loaded."""
        self.expect_visible(self.DASHBOARD_HEADER)
        self.expect_visible(self.LOGOUT_BUTTON)

    def expect_logged_in(self):
        """Assert that user is logged in."""
        self.expect_visible(self.LOGOUT_BUTTON)
        self.expect_url('/dashboard')

    def expect_portfolio_summary_visible(self):
        """Assert that portfolio summary is visible."""
        # At least one of these should be visible
        assert self.is_portfolio_summary_displayed(), "Portfolio summary should be visible"

    def expect_navigation_visible(self):
        """Assert that navigation is visible."""
        self.expect_visible(self.NAVIGATION_MENU)
