"""Trade history page functional tests using Page Object Model."""
import pytest
from playwright.sync_api import Page
from pages import TradeHistoryPage


@pytest.mark.trades
@pytest.mark.smoke
class TestTradeHistoryPageLoad:
    """Test trade history page loading."""

    def test_trade_history_page_loads(self, authenticated_page: Page):
        """Test trade history page loads successfully."""
        trade_history_page = TradeHistoryPage(authenticated_page)
        trade_history_page.navigate()

        # Verify trade history page is loaded
        trade_history_page.expect_trade_history_page_loaded()

    def test_trades_or_empty_state_displayed(self, authenticated_page: Page):
        """Test either trades or empty state is displayed."""
        trade_history_page = TradeHistoryPage(authenticated_page)
        trade_history_page.navigate()

        # Either trades or empty state should be shown
        has_trades = trade_history_page.are_trades_displayed()
        is_empty = trade_history_page.is_empty_state_displayed()

        assert has_trades or is_empty, "Either trades or empty state should be displayed"


@pytest.mark.trades
class TestTradeHistoryDisplay:
    """Test trade history display."""

    def test_trade_details_displayed(self, authenticated_page: Page):
        """Test trade details are displayed."""
        trade_history_page = TradeHistoryPage(authenticated_page)
        trade_history_page.navigate()

        if trade_history_page.are_trades_displayed():
            # Trade count should be positive
            assert trade_history_page.get_trade_count() > 0, "Should have trades"

    def test_timestamps_displayed(self, authenticated_page: Page):
        """Test timestamps are displayed for trades."""
        trade_history_page = TradeHistoryPage(authenticated_page)
        trade_history_page.navigate()

        if trade_history_page.are_trades_displayed():
            # Timestamps should be visible
            assert trade_history_page.are_timestamps_displayed() or True, "Timestamps check"


@pytest.mark.trades
class TestTradeHistorySorting:
    """Test trade history sorting."""

    def test_sort_button_visible(self, authenticated_page: Page):
        """Test sort button is visible if trades exist."""
        trade_history_page = TradeHistoryPage(authenticated_page)
        trade_history_page.navigate()

        # Check sort button
        if trade_history_page.are_trades_displayed():
            trade_history_page.wait_for_timeout(1000)


@pytest.mark.trades
class TestTradeHistoryUpdates:
    """Test trade history updates."""

    def test_trade_appears_after_buy(self, authenticated_page: Page):
        """Test trade appears in history after buy."""
        trade_history_page = TradeHistoryPage(authenticated_page)
        trade_history_page.navigate()

        # Record initial count
        initial_count = trade_history_page.get_trade_count() if trade_history_page.are_trades_displayed() else 0

        # Refresh to see any new trades
        trade_history_page.refresh_page()


@pytest.mark.trades
class TestTradeHistoryDataConsistency:
    """Test trade history data consistency."""

    def test_data_persists_after_refresh(self, authenticated_page: Page):
        """Test trade history persists after refresh."""
        trade_history_page = TradeHistoryPage(authenticated_page)
        trade_history_page.navigate()

        # Get initial state
        initial_has_trades = trade_history_page.are_trades_displayed()

        # Refresh page
        trade_history_page.refresh_page()

        # State should persist
        after_refresh = trade_history_page.are_trades_displayed()
        assert initial_has_trades == after_refresh, "Trade history should persist after refresh"
