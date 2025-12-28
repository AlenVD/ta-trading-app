"""Trade history page object."""
from typing import List, Optional
from playwright.sync_api import Page
from .base_page import BasePage


class TradeHistoryPage(BasePage):
    """Trade history page object with trade history-specific functionality."""

    # Locators
    PAGE_HEADER = 'text=/trade history|trades/i'
    TRADE_ROW = '[data-testid="trade-row"], tr'
    TRADE_TYPE = 'text=/BUY|SELL/i'
    STOCK_SYMBOL = 'text=/AAPL|GOOGL|MSFT|TSLA|NVDA/i'
    QUANTITY_CELL = 'td:has-text("shares"), td'
    PRICE_CELL = 'text=/\$/i'
    TIMESTAMP_CELL = 'text=/ago|AM|PM|:/i'
    SORT_BUTTON = 'button:has-text(/sort|date/i)'
    FILTER_BUTTON = 'button:has-text(/filter/i)'
    PAGINATION = 'text=/page|next|previous/i'
    EMPTY_STATE = 'text=/no trades|no history|empty/i'

    def __init__(self, page: Page):
        """Initialize trade history page.

        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = self.settings.trades_url

    def navigate(self):
        """Navigate to trade history page."""
        self.goto(self.url)
        self.wait_for_url('/trades')

    def is_loaded(self) -> bool:
        """Check if trade history page is fully loaded.

        Returns:
            True if page is loaded, False otherwise
        """
        self.wait_for_timeout(2000)
        return self.is_visible(self.PAGE_HEADER)

    def are_trades_displayed(self) -> bool:
        """Check if trades are displayed.

        Returns:
            True if trades are visible, False otherwise
        """
        return self.element_count(self.TRADE_TYPE) > 0

    def get_trade_count(self) -> int:
        """Get number of trades displayed.

        Returns:
            Number of trades
        """
        return self.element_count(self.TRADE_TYPE)

    def is_empty_state_displayed(self) -> bool:
        """Check if empty state is displayed.

        Returns:
            True if empty state is visible, False otherwise
        """
        return self.is_visible(self.EMPTY_STATE)

    def is_trade_type_displayed(self, trade_type: str) -> bool:
        """Check if specific trade type is displayed.

        Args:
            trade_type: Trade type (BUY or SELL)

        Returns:
            True if trade type is visible, False otherwise
        """
        return self.is_visible(f'text="{trade_type}"')

    def is_symbol_displayed(self, symbol: str) -> bool:
        """Check if specific symbol is displayed.

        Args:
            symbol: Stock symbol

        Returns:
            True if symbol is visible, False otherwise
        """
        return self.is_visible(f'text="{symbol}"')

    def are_timestamps_displayed(self) -> bool:
        """Check if timestamps are displayed.

        Returns:
            True if timestamps are visible, False otherwise
        """
        return self.element_count(self.TIMESTAMP_CELL) > 0

    def is_sort_button_visible(self) -> bool:
        """Check if sort button is visible.

        Returns:
            True if sort button is visible, False otherwise
        """
        return self.is_visible(self.SORT_BUTTON)

    def click_sort(self):
        """Click sort button."""
        if self.is_sort_button_visible():
            self.click(self.SORT_BUTTON)
            self.wait_for_timeout(1000)

    def is_pagination_visible(self) -> bool:
        """Check if pagination is visible.

        Returns:
            True if pagination is visible, False otherwise
        """
        return self.is_visible(self.PAGINATION)

    def refresh_page(self):
        """Refresh trade history page."""
        self.page.reload()
        self.wait_for_load_state('networkidle')

    # Validation methods
    def expect_trade_history_page_loaded(self):
        """Assert that trade history page is loaded."""
        self.expect_visible(self.PAGE_HEADER)
        self.expect_url('/trades')

    def expect_trades_displayed(self):
        """Assert that trades are displayed."""
        assert self.are_trades_displayed(), "Trades should be displayed"

    def expect_trade_appears(self, trade_type: str, symbol: str):
        """Assert that specific trade appears.

        Args:
            trade_type: Trade type (BUY or SELL)
            symbol: Stock symbol
        """
        assert self.is_trade_type_displayed(trade_type), f"{trade_type} trade should be displayed"
        assert self.is_symbol_displayed(symbol), f"Symbol {symbol} should be displayed"

    def expect_empty_state(self):
        """Assert that empty state is displayed."""
        self.expect_visible(self.EMPTY_STATE)
