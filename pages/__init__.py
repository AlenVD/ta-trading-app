"""Page Object Model package for test framework."""
from .base_page import BasePage
from .login_page import LoginPage
from .dashboard_page import DashboardPage
from .trading_page import TradingPage
from .portfolio_page import PortfolioPage
from .watchlist_page import WatchlistPage
from .trade_history_page import TradeHistoryPage

__all__ = [
    'BasePage',
    'LoginPage',
    'DashboardPage',
    'TradingPage',
    'PortfolioPage',
    'WatchlistPage',
    'TradeHistoryPage'
]
