"""Portfolio page object."""
from typing import List, Optional
from playwright.sync_api import Page
from .base_page import BasePage
from models.stock import Stock


class PortfolioPage(BasePage):
    """Portfolio page object with portfolio-specific functionality."""

    # Locators
    PAGE_HEADER = 'text=/portfolio/i'
    POSITION_ROW = '[data-testid="position-row"], tr'
    STOCK_SYMBOL = 'text=/AAPL|GOOGL|MSFT|TSLA|NVDA/i'
    QUANTITY_CELL = 'text=/shares|qty/i'
    VALUE_CELL = 'text=/value|\$/i'
    PROFIT_LOSS_CELL = 'text=/p&l|profit|loss/i'
    COST_BASIS_CELL = 'text=/cost basis|avg cost/i'
    TRADE_BUTTON = 'button:has-text(/trade/i)'
    STOCK_DETAILS_BUTTON = 'button:has-text(/details|view/i)'
    PORTFOLIO_METRICS = 'text=/total value|portfolio value/i'
    EMPTY_STATE = 'text=/no positions|no holdings|empty/i'

    def __init__(self, page: Page):
        """Initialize portfolio page.

        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = self.settings.portfolio_url

    def navigate(self):
        """Navigate to portfolio page."""
        self.goto(self.url)
        self.wait_for_url('/portfolio')

    def is_loaded(self) -> bool:
        """Check if portfolio page is fully loaded.

        Returns:
            True if page is loaded, False otherwise
        """
        return self.is_visible(self.PAGE_HEADER)

    def are_positions_displayed(self) -> bool:
        """Check if positions are displayed.

        Returns:
            True if positions are visible, False otherwise
        """
        return self.element_count(self.STOCK_SYMBOL) > 0

    def get_position_count(self) -> int:
        """Get number of positions displayed.

        Returns:
            Number of positions
        """
        return self.element_count(self.STOCK_SYMBOL)

    def is_empty_state_displayed(self) -> bool:
        """Check if empty state is displayed.

        Returns:
            True if empty state is visible, False otherwise
        """
        return self.is_visible(self.EMPTY_STATE)

    def are_metrics_displayed(self) -> bool:
        """Check if portfolio metrics are displayed.

        Returns:
            True if metrics are visible, False otherwise
        """
        return self.is_visible(self.PORTFOLIO_METRICS)

    def get_portfolio_value(self) -> Optional[float]:
        """Get portfolio value from metrics.

        Returns:
            Portfolio value or None
        """
        if self.are_metrics_displayed():
            text = self.get_text(self.PORTFOLIO_METRICS)
            return self.extract_number_from_text(text) if text else None
        return None

    def are_trade_buttons_visible(self) -> bool:
        """Check if trade buttons are visible for positions.

        Returns:
            True if trade buttons are visible, False otherwise
        """
        return self.element_count(self.TRADE_BUTTON) > 0

    def click_trade_button_for_position(self, index: int = 0):
        """Click trade button for specific position.

        Args:
            index: Position index (0-based)
        """
        buttons = self.find_element(self.TRADE_BUTTON)
        if buttons.count() > index:
            buttons.nth(index).click()

    def refresh_page(self):
        """Refresh portfolio page."""
        self.page.reload()
        self.wait_for_load_state('networkidle')

    # Validation methods
    def expect_portfolio_page_loaded(self):
        """Assert that portfolio page is loaded."""
        self.expect_visible(self.PAGE_HEADER)
        self.expect_url('/portfolio')

    def expect_positions_displayed(self):
        """Assert that positions are displayed."""
        assert self.are_positions_displayed(), "Positions should be displayed"

    def expect_metrics_displayed(self):
        """Assert that portfolio metrics are displayed."""
        assert self.are_metrics_displayed(), "Portfolio metrics should be displayed"

    def expect_empty_state(self):
        """Assert that empty state is displayed."""
        self.expect_visible(self.EMPTY_STATE)
