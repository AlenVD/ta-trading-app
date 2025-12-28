"""Watchlist page object."""
from typing import Optional
from playwright.sync_api import Page
from .base_page import BasePage


class WatchlistPage(BasePage):
    """Watchlist page object with watchlist-specific functionality."""

    # Locators
    PAGE_HEADER = 'text=/watchlist/i'
    CREATE_WATCHLIST_BUTTON = 'button:has-text(/create|new watchlist/i)'
    WATCHLIST_NAME_INPUT = 'input[type="text"], input[placeholder*="name"]'
    SAVE_BUTTON = 'button:has-text(/save|create/i)'
    CANCEL_BUTTON = 'button:has-text(/cancel|close/i)'
    WATCHLIST_ITEM = '[data-testid="watchlist-item"], .watchlist-item'
    ADD_STOCK_BUTTON = 'button:has-text(/add stock|add/i)'
    STOCK_SYMBOL_INPUT = 'input[placeholder*="symbol"], input[placeholder*="stock"]'
    REMOVE_STOCK_BUTTON = 'button:has-text(/remove|delete/i)'
    DELETE_WATCHLIST_BUTTON = 'button:has-text(/delete watchlist/i)'
    SUCCESS_MESSAGE = 'text=/success|added|created/i'
    ERROR_MESSAGE = 'text=/error|failed|already exists/i'

    def __init__(self, page: Page):
        """Initialize watchlist page.

        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = self.settings.watchlists_url

    def navigate(self):
        """Navigate to watchlist page."""
        self.goto(self.url)
        self.wait_for_url('/watchlists')

    def is_loaded(self) -> bool:
        """Check if watchlist page is fully loaded.

        Returns:
            True if page is loaded, False otherwise
        """
        self.wait_for_timeout(2000)
        return self.is_visible(self.PAGE_HEADER)

    def is_create_button_visible(self) -> bool:
        """Check if create watchlist button is visible.

        Returns:
            True if button is visible, False otherwise
        """
        return self.is_visible(self.CREATE_WATCHLIST_BUTTON)

    def click_create_watchlist(self):
        """Click create watchlist button."""
        self.click(self.CREATE_WATCHLIST_BUTTON)
        self.wait_for_timeout(1000)

    def fill_watchlist_name(self, name: str):
        """Fill watchlist name input.

        Args:
            name: Watchlist name
        """
        self.fill(self.WATCHLIST_NAME_INPUT, name)

    def click_save(self):
        """Click save button."""
        if self.element_count(self.SAVE_BUTTON) > 0:
            self.find_element(self.SAVE_BUTTON).first.click()
            self.wait_for_timeout(1000)

    def create_watchlist(self, name: str):
        """Create a new watchlist.

        Args:
            name: Watchlist name
        """
        self.click_create_watchlist()
        self.fill_watchlist_name(name)
        self.click_save()

    def get_watchlist_count(self) -> int:
        """Get number of watchlists.

        Returns:
            Number of watchlists
        """
        return self.element_count(self.WATCHLIST_ITEM)

    def is_watchlist_displayed(self, name: str) -> bool:
        """Check if watchlist with name is displayed.

        Args:
            name: Watchlist name

        Returns:
            True if watchlist is displayed, False otherwise
        """
        return self.is_visible(f'text="{name}"')

    def click_add_stock(self):
        """Click add stock button."""
        if self.element_count(self.ADD_STOCK_BUTTON) > 0:
            self.find_element(self.ADD_STOCK_BUTTON).first.click()
            self.wait_for_timeout(1000)

    def fill_stock_symbol(self, symbol: str):
        """Fill stock symbol input.

        Args:
            symbol: Stock symbol
        """
        self.fill(self.STOCK_SYMBOL_INPUT, symbol)

    def add_stock_to_watchlist(self, symbol: str):
        """Add stock to watchlist.

        Args:
            symbol: Stock symbol
        """
        self.click_add_stock()
        self.fill_stock_symbol(symbol)
        self.click_save()

    def is_stock_in_watchlist(self, symbol: str) -> bool:
        """Check if stock is in watchlist.

        Args:
            symbol: Stock symbol

        Returns:
            True if stock is in watchlist, False otherwise
        """
        return self.is_visible(f'text="{symbol}"')

    def remove_first_stock(self):
        """Remove first stock from watchlist."""
        if self.element_count(self.REMOVE_STOCK_BUTTON) > 0:
            self.find_element(self.REMOVE_STOCK_BUTTON).first.click()
            self.wait_for_timeout(1000)

    def delete_first_watchlist(self):
        """Delete first watchlist."""
        if self.element_count(self.DELETE_WATCHLIST_BUTTON) > 0:
            self.find_element(self.DELETE_WATCHLIST_BUTTON).first.click()
            self.wait_for_timeout(1000)

    def is_success_message_displayed(self) -> bool:
        """Check if success message is displayed.

        Returns:
            True if success message is visible, False otherwise
        """
        return self.is_visible(self.SUCCESS_MESSAGE)

    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed.

        Returns:
            True if error message is visible, False otherwise
        """
        return self.is_visible(self.ERROR_MESSAGE)

    # Validation methods
    def expect_watchlist_page_loaded(self):
        """Assert that watchlist page is loaded."""
        self.expect_visible(self.PAGE_HEADER)
        self.expect_url('/watchlists')

    def expect_create_button_visible(self):
        """Assert that create button is visible."""
        self.expect_visible(self.CREATE_WATCHLIST_BUTTON)

    def expect_watchlist_created(self, name: str):
        """Assert that watchlist was created.

        Args:
            name: Watchlist name
        """
        assert self.is_watchlist_displayed(name), f"Watchlist '{name}' should be displayed"
