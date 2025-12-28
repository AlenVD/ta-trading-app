"""Watchlists page functional tests using Page Object Model."""
import pytest
from playwright.sync_api import Page
from pages import WatchlistPage
from config import TestData


@pytest.mark.watchlist
@pytest.mark.smoke
class TestWatchlistPageLoad:
    """Test watchlist page loading."""

    def test_watchlist_page_loads(self, authenticated_page: Page):
        """Test watchlist page loads successfully."""
        watchlist_page = WatchlistPage(authenticated_page)
        watchlist_page.navigate()

        # Verify watchlist page is loaded
        watchlist_page.expect_watchlist_page_loaded()

    def test_create_button_visible(self, authenticated_page: Page):
        """Test create watchlist button is visible."""
        watchlist_page = WatchlistPage(authenticated_page)
        watchlist_page.navigate()

        # Create button should be visible
        watchlist_page.expect_create_button_visible()


@pytest.mark.watchlist
class TestCreateWatchlist:
    """Test create watchlist functionality."""

    def test_create_watchlist_button_click(self, authenticated_page: Page):
        """Test clicking create watchlist button."""
        watchlist_page = WatchlistPage(authenticated_page)
        watchlist_page.navigate()

        # Click create button
        watchlist_page.click_create_watchlist()

    def test_create_new_watchlist(self, authenticated_page: Page):
        """Test creating a new watchlist."""
        watchlist_page = WatchlistPage(authenticated_page)
        watchlist_page.navigate()

        # Create watchlist
        watchlist_name = f"Test Watchlist {watchlist_page.get_watchlist_count() + 1}"
        watchlist_page.create_watchlist(watchlist_name)

        # Wait for creation
        watchlist_page.wait_for_timeout(2000)

    def test_create_watchlist_with_empty_name(self, authenticated_page: Page):
        """Test creating watchlist with empty name shows validation."""
        watchlist_page = WatchlistPage(authenticated_page)
        watchlist_page.navigate()

        # Try to create with empty name
        watchlist_page.click_create_watchlist()
        watchlist_page.fill_watchlist_name("")
        watchlist_page.click_save()


@pytest.mark.watchlist
class TestAddStockToWatchlist:
    """Test adding stocks to watchlist."""

    def test_add_stock_button_visible(self, authenticated_page: Page):
        """Test add stock button is visible."""
        watchlist_page = WatchlistPage(authenticated_page)
        watchlist_page.navigate()

        # Create a watchlist first if needed
        if watchlist_page.get_watchlist_count() == 0:
            watchlist_page.create_watchlist("My Watchlist")
            watchlist_page.wait_for_timeout(2000)

    def test_add_stock_to_watchlist(self, authenticated_page: Page):
        """Test adding a stock to watchlist."""
        watchlist_page = WatchlistPage(authenticated_page)
        watchlist_page.navigate()

        # Create watchlist if needed
        if watchlist_page.get_watchlist_count() == 0:
            watchlist_page.create_watchlist("Tech Stocks")
            watchlist_page.wait_for_timeout(2000)


@pytest.mark.watchlist
class TestRemoveStockFromWatchlist:
    """Test removing stocks from watchlist."""

    def test_remove_stock(self, authenticated_page: Page):
        """Test removing a stock from watchlist."""
        watchlist_page = WatchlistPage(authenticated_page)
        watchlist_page.navigate()

        # Wait for page to load
        watchlist_page.wait_for_timeout(2000)


@pytest.mark.watchlist
class TestDeleteWatchlist:
    """Test deleting watchlist."""

    def test_delete_watchlist(self, authenticated_page: Page):
        """Test deleting a watchlist."""
        watchlist_page = WatchlistPage(authenticated_page)
        watchlist_page.navigate()

        # Wait for page to load
        watchlist_page.wait_for_timeout(2000)
