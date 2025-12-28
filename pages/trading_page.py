"""Trading page object."""
from typing import Optional
from playwright.sync_api import Page
from .base_page import BasePage
from models.trade import Trade, TradeType


class TradingPage(BasePage):
    """Trading page object with trading-specific functionality."""

    # Locators
    PAGE_HEADER = 'text=/trading|trade stocks/i'
    TRADE_BUTTON = 'button:has-text("Trade")'
    BUY_BUTTON = 'text=BUY'
    SELL_BUTTON = 'text=SELL'
    QUANTITY_INPUT = 'input[type="number"]'
    EXECUTE_BUTTON = 'button:has-text(/execute|buy|sell|confirm/i)'
    CANCEL_BUTTON = 'button:has-text(/cancel|close/i)'
    SUCCESS_MESSAGE = 'text=/success|completed|executed/i'
    ERROR_MESSAGE = 'text=/error|failed|insufficient/i'
    STOCK_SYMBOLS = 'text=/AAPL|GOOGL|MSFT|TSLA|NVDA/i'

    def __init__(self, page: Page):
        """Initialize trading page.

        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        self.url = self.settings.trading_url

    def navigate(self):
        """Navigate to trading page."""
        self.goto(self.url)
        self.wait_for_url('/trading')

    def is_loaded(self) -> bool:
        """Check if trading page is fully loaded.

        Returns:
            True if page is loaded, False otherwise
        """
        self.wait_for_timeout(2000)  # Wait for stocks to load
        return self.is_visible(self.PAGE_HEADER)

    def are_stocks_displayed(self) -> bool:
        """Check if stocks are displayed.

        Returns:
            True if stocks are visible, False otherwise
        """
        return self.element_count(self.STOCK_SYMBOLS) > 0

    def are_trade_buttons_visible(self) -> bool:
        """Check if trade buttons are visible.

        Returns:
            True if trade buttons are visible, False otherwise
        """
        return self.element_count(self.TRADE_BUTTON) > 0

    def click_first_trade_button(self):
        """Click the first trade button."""
        self.wait_for_timeout(2000)
        if self.are_trade_buttons_visible():
            self.find_element(self.TRADE_BUTTON).first.click()
            self.wait_for_timeout(1000)

    def click_trade_button_for_symbol(self, symbol: str):
        """Click trade button for specific stock symbol.

        Args:
            symbol: Stock symbol (e.g., 'AAPL')
        """
        button_selector = f'button:has-text("Trade"):near(text="{symbol}")'
        self.click(button_selector)
        self.wait_for_timeout(1000)

    def is_trade_modal_open(self) -> bool:
        """Check if trade modal is open.

        Returns:
            True if modal is open, False otherwise
        """
        return self.is_visible(self.BUY_BUTTON) and self.is_visible(self.SELL_BUTTON)

    def select_buy(self):
        """Select BUY option in trade modal."""
        self.click(self.BUY_BUTTON)

    def select_sell(self):
        """Select SELL option in trade modal."""
        self.click(self.SELL_BUTTON)

    def fill_quantity(self, quantity: int):
        """Fill trade quantity.

        Args:
            quantity: Number of shares
        """
        if self.element_count(self.QUANTITY_INPUT) > 0:
            self.fill(self.QUANTITY_INPUT, str(quantity))

    def click_execute(self):
        """Click execute button to submit trade."""
        if self.element_count(self.EXECUTE_BUTTON) > 0:
            self.find_element(self.EXECUTE_BUTTON).first.click()

    def click_cancel(self):
        """Click cancel button to close modal."""
        if self.element_count(self.CANCEL_BUTTON) > 0:
            self.find_element(self.CANCEL_BUTTON).first.click()

    def execute_buy_trade(self, quantity: int, wait_for_success: bool = True):
        """Execute a buy trade.

        Args:
            quantity: Number of shares to buy
            wait_for_success: Whether to wait for success message
        """
        self.click_first_trade_button()
        self.select_buy()
        self.fill_quantity(quantity)
        self.click_execute()

        if wait_for_success:
            self.wait_for_timeout(2000)

    def execute_sell_trade(self, quantity: int, wait_for_success: bool = True):
        """Execute a sell trade.

        Args:
            quantity: Number of shares to sell
            wait_for_success: Whether to wait for success message
        """
        self.click_first_trade_button()
        self.select_sell()
        self.fill_quantity(quantity)
        self.click_execute()

        if wait_for_success:
            self.wait_for_timeout(2000)

    def execute_trade(self, trade: Trade, wait_for_success: bool = True):
        """Execute a trade using Trade model.

        Args:
            trade: Trade object with type and quantity
            wait_for_success: Whether to wait for success message
        """
        if trade.trade_type == TradeType.BUY:
            self.execute_buy_trade(trade.quantity, wait_for_success)
        else:
            self.execute_sell_trade(trade.quantity, wait_for_success)

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

    def is_quantity_input_visible(self) -> bool:
        """Check if quantity input is visible.

        Returns:
            True if quantity input is visible, False otherwise
        """
        return self.element_count(self.QUANTITY_INPUT) > 0

    def is_execute_button_visible(self) -> bool:
        """Check if execute button is visible.

        Returns:
            True if execute button is visible, False otherwise
        """
        return self.element_count(self.EXECUTE_BUTTON) > 0

    # Validation methods
    def expect_trading_page_loaded(self):
        """Assert that trading page is loaded."""
        self.expect_visible(self.PAGE_HEADER)
        self.expect_url('/trading')

    def expect_stocks_displayed(self):
        """Assert that stocks are displayed."""
        self.wait_for_timeout(2000)
        assert self.are_stocks_displayed(), "Stocks should be displayed"

    def expect_trade_modal_open(self):
        """Assert that trade modal is open."""
        self.expect_visible(self.BUY_BUTTON)
        self.expect_visible(self.SELL_BUTTON)

    def expect_trade_form_elements(self):
        """Assert that trade form elements are visible."""
        assert self.is_quantity_input_visible(), "Quantity input should be visible"
        assert self.is_execute_button_visible(), "Execute button should be visible"
