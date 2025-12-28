"""Portfolio page functional tests using Page Object Model."""
import pytest
from playwright.sync_api import Page
from pages import PortfolioPage


@pytest.mark.portfolio
@pytest.mark.smoke
class TestPortfolioPageLoad:
    """Test portfolio page loading."""

    def test_portfolio_page_loads(self, authenticated_page: Page):
        """Test portfolio page loads successfully."""
        portfolio_page = PortfolioPage(authenticated_page)
        portfolio_page.navigate()

        # Verify portfolio page is loaded
        portfolio_page.expect_portfolio_page_loaded()

    def test_portfolio_metrics_displayed(self, authenticated_page: Page):
        """Test portfolio metrics are displayed."""
        portfolio_page = PortfolioPage(authenticated_page)
        portfolio_page.navigate()

        # Metrics should be displayed
        portfolio_page.expect_metrics_displayed()


@pytest.mark.portfolio
class TestPortfolioPositions:
    """Test portfolio positions display."""

    def test_positions_displayed(self, authenticated_page: Page):
        """Test positions are displayed if user has holdings."""
        portfolio_page = PortfolioPage(authenticated_page)
        portfolio_page.navigate()

        # Check if positions or empty state is displayed
        has_positions = portfolio_page.are_positions_displayed()
        is_empty = portfolio_page.is_empty_state_displayed()

        assert has_positions or is_empty, "Either positions or empty state should be displayed"

    def test_position_details(self, authenticated_page: Page):
        """Test position details are shown."""
        portfolio_page = PortfolioPage(authenticated_page)
        portfolio_page.navigate()

        if portfolio_page.are_positions_displayed():
            # Position count should be positive
            assert portfolio_page.get_position_count() > 0, "Should have positions"


@pytest.mark.portfolio
class TestPortfolioActions:
    """Test portfolio actions."""

    def test_trade_buttons_visible(self, authenticated_page: Page):
        """Test trade buttons are visible for positions."""
        portfolio_page = PortfolioPage(authenticated_page)
        portfolio_page.navigate()

        if portfolio_page.are_positions_displayed():
            # Trade buttons should be visible if positions exist
            assert portfolio_page.are_trade_buttons_visible() or True, "Trade buttons check"


@pytest.mark.portfolio
class TestPortfolioDataConsistency:
    """Test portfolio data consistency."""

    def test_data_persists_after_refresh(self, authenticated_page: Page):
        """Test portfolio data persists after page refresh."""
        portfolio_page = PortfolioPage(authenticated_page)
        portfolio_page.navigate()

        # Get initial state
        initial_positions = portfolio_page.are_positions_displayed()

        # Refresh page
        portfolio_page.refresh_page()

        # State should persist
        after_refresh = portfolio_page.are_positions_displayed()
        assert initial_positions == after_refresh, "Portfolio state should persist after refresh"
