"""Trading page functional tests using Page Object Model."""
import pytest
from playwright.sync_api import Page
from pages import TradingPage
from models import Trade, TradeType
from config import TestData


@pytest.mark.trading
@pytest.mark.smoke
class TestTradingPageLoad:
    """Test trading page loading."""

    def test_trading_page_loads(self, authenticated_page: Page):
        """Test trading page loads successfully."""
        trading_page = TradingPage(authenticated_page)
        trading_page.navigate()

        # Verify trading page is loaded
        trading_page.expect_trading_page_loaded()

    def test_stocks_list_displayed(self, authenticated_page: Page):
        """Test stocks list is displayed."""
        trading_page = TradingPage(authenticated_page)
        trading_page.navigate()

        # Stocks should be displayed
        trading_page.expect_stocks_displayed()

    def test_trade_buttons_visible(self, authenticated_page: Page):
        """Test trade buttons are visible for stocks."""
        trading_page = TradingPage(authenticated_page)
        trading_page.navigate()

        # Trade buttons should be visible
        assert trading_page.are_trade_buttons_visible(), "Trade buttons should be visible"


@pytest.mark.trading
class TestBuyTrade:
    """Test buy trade functionality."""

    def test_open_buy_trade_modal(self, authenticated_page: Page):
        """Test opening buy trade modal."""
        trading_page = TradingPage(authenticated_page)
        trading_page.navigate()

        # Open trade modal
        trading_page.click_first_trade_button()

        # Modal should be open
        trading_page.expect_trade_modal_open()

    def test_buy_trade_form_elements(self, authenticated_page: Page):
        """Test buy trade form has required elements."""
        trading_page = TradingPage(authenticated_page)
        trading_page.navigate()

        # Open trade modal and select BUY
        trading_page.click_first_trade_button()
        trading_page.select_buy()

        # Form elements should be visible
        trading_page.expect_trade_form_elements()

    def test_execute_buy_trade(self, authenticated_page: Page):
        """Test executing a buy trade."""
        trading_page = TradingPage(authenticated_page)
        trading_page.navigate()

        # Execute buy trade
        trading_page.execute_buy_trade(quantity=TestData.DEFAULT_TRADE_QUANTITY)

        # Wait for completion
        trading_page.wait_for_timeout(2000)

    def test_cancel_buy_trade(self, authenticated_page: Page):
        """Test canceling a buy trade."""
        trading_page = TradingPage(authenticated_page)
        trading_page.navigate()

        # Open trade modal
        trading_page.click_first_trade_button()
        trading_page.select_buy()

        # Cancel trade
        trading_page.click_cancel()


@pytest.mark.trading
class TestSellTrade:
    """Test sell trade functionality."""

    def test_execute_sell_trade(self, authenticated_page: Page):
        """Test executing a sell trade."""
        trading_page = TradingPage(authenticated_page)
        trading_page.navigate()

        # Execute sell trade
        trading_page.execute_sell_trade(quantity=TestData.SMALL_TRADE_QUANTITY)

        # Wait for completion
        trading_page.wait_for_timeout(2000)


@pytest.mark.trading
class TestTradingWorkflows:
    """Test complete trading workflows."""

    def test_buy_sell_cycle(self, authenticated_page: Page):
        """Test complete buy-sell cycle."""
        trading_page = TradingPage(authenticated_page)
        trading_page.navigate()

        # Buy shares
        trading_page.execute_buy_trade(quantity=TestData.DEFAULT_TRADE_QUANTITY)
        trading_page.wait_for_timeout(3000)

        # Sell shares
        trading_page.navigate()
        trading_page.execute_sell_trade(quantity=TestData.SMALL_TRADE_QUANTITY)
        trading_page.wait_for_timeout(3000)
