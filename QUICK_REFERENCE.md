# Quick Reference Guide

Fast reference for common tasks in the refactored automation framework.

## Daily Commands

```bash
# Setup (first time only)
make setup

# Run all tests
make test-smoke          # All smoke tests (~30 seconds)
make test                # All tests (~5-10 minutes)
make test-parallel       # All tests in parallel (faster)

# Run module-specific tests
make test-auth           # All authentication tests
make test-trading        # All trading tests
make test-portfolio      # All portfolio tests
make test-watchlist      # All watchlist tests
make test-dashboard      # All dashboard tests
make test-trades         # All trade history tests

# Run module-specific SMOKE tests
make test-smoke-auth     # Auth smoke tests only
make test-smoke-trading  # Trading smoke tests only
make test-smoke-portfolio # Portfolio smoke tests only
make test-smoke-watchlist # Watchlist smoke tests only
make test-smoke-dashboard # Dashboard smoke tests only
make test-smoke-trades   # Trade history smoke tests only

# View results
make report              # Open HTML report in browser

# Clean up
make clean               # Remove reports and cache
```

## Project Structure at a Glance

```
ta-trading-app/
├── Makefile            → Test commands
├── pytest.ini          → Pytest configuration
├── conftest.py         → Test fixtures
├── config/             → Settings & test data
├── models/             → Data classes (User, Trade, Stock)
├── pages/              → Page objects (LoginPage, etc.)
├── tests/              → Test files
└── utils/              → Helper functions
```

## Writing a Test

```python
"""Template for new test."""
import pytest
from playwright.sync_api import Page
from pages import LoginPage, DashboardPage  # Import page objects
from config import TestData                 # Import test data

@pytest.mark.smoke                          # Add marker
class TestMyFeature:                        # Class per feature
    """Test my feature."""
    
    def test_something(self, page: Page):   # Test method
        """Test description."""
        # 1. Create page objects
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)
        
        # 2. Perform actions
        login_page.navigate()
        login_page.login(TestData.PRIMARY_USER)
        
        # 3. Verify results
        dashboard_page.expect_logged_in()
```

## Creating a Page Object

```python
"""Template for new page object."""
from playwright.sync_api import Page
from .base_page import BasePage

class MyPage(BasePage):
    """My page object."""
    
    # 1. Define locators as constants
    BUTTON = 'button#submit'
    INPUT = 'input[name="email"]'
    HEADING = 'h1.title'
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.settings.base_url + '/mypage'
    
    # 2. Navigation methods
    def navigate(self):
        """Navigate to page."""
        self.goto(self.url)
    
    # 3. Action methods
    def fill_input(self, value: str):
        """Fill input field."""
        self.fill(self.INPUT, value)
    
    def click_button(self):
        """Click submit button."""
        self.click(self.BUTTON)
    
    # 4. Validation methods
    def expect_page_loaded(self):
        """Assert page is loaded."""
        self.expect_visible(self.HEADING)
```

## Accessing Configuration

```python
from config import settings, TestData

# URLs
settings.base_url           # http://localhost:5173
settings.login_url          # http://localhost:5173/login
settings.dashboard_url      # http://localhost:5173/dashboard

# Test data
user = TestData.PRIMARY_USER              # Main test user
users = TestData.get_all_users()          # All test users
quantity = TestData.DEFAULT_TRADE_QUANTITY  # 10
```

## Using Data Models

```python
from models import User, Trade, TradeType

# Create user
user = User(
    email='test@example.com',
    password='password123',
    name='Test User'
)

# Create trade
trade = Trade(
    symbol='AAPL',
    quantity=10,
    trade_type=TradeType.BUY,
    price=150.00
)
```

## Common Page Object Methods

All page objects inherit these from `BasePage`:

```python
# Navigation
page_obj.goto(url)
page_obj.navigate()
page_obj.wait_for_url(url)

# Element interaction
page_obj.click(selector)
page_obj.fill(selector, value)
page_obj.get_text(selector)

# Waiting
page_obj.wait_for_element(selector)
page_obj.wait_for_timeout(ms)

# Assertions
page_obj.expect_visible(selector)
page_obj.expect_hidden(selector)
page_obj.expect_text(selector, text)
page_obj.expect_url(url)

# Utilities
page_obj.take_screenshot(name)
page_obj.get_local_storage_item(key)
page_obj.extract_number_from_text(text)
```

## Available Page Objects

```python
from pages import (
    LoginPage,           # login_page.navigate(), login(), expect_login_page_loaded()
    DashboardPage,       # navigate(), logout(), expect_logged_in()
    TradingPage,         # navigate(), execute_buy_trade(), execute_sell_trade()
    PortfolioPage,       # navigate(), expect_positions_displayed()
    WatchlistPage,       # navigate(), create_watchlist(), add_stock()
    TradeHistoryPage     # navigate(), expect_trades_displayed()
)
```

## Test Markers

```python
@pytest.mark.smoke       # Quick smoke tests
@pytest.mark.auth        # Authentication tests
@pytest.mark.trading     # Trading tests
@pytest.mark.portfolio   # Portfolio tests
@pytest.mark.watchlist   # Watchlist tests
@pytest.mark.dashboard   # Dashboard tests
@pytest.mark.trades      # Trade history tests
@pytest.mark.regression  # Regression tests
```

## Fixtures

```python
def test_example(self, page: Page):
    # Fresh page for each test
    
def test_example(self, authenticated_page: Page):
    # Already logged in, use for protected pages
```

## Make Commands Reference

```bash
# Setup
make setup               # Full setup (one time)
make install             # Install dependencies only
make browsers            # Install browsers only

# All Tests
make test                # All tests
make test-smoke          # All smoke tests
make test-regression     # Regression tests
make test-parallel       # Parallel execution

# Module-Specific Tests (All tests in module)
make test-auth           # All auth tests
make test-trading        # All trading tests
make test-portfolio      # All portfolio tests
make test-watchlist      # All watchlist tests
make test-dashboard      # All dashboard tests
make test-trades         # All trade history tests

# Module-Specific Smoke Tests (Smoke tests only)
make test-smoke-auth     # Auth smoke tests only
make test-smoke-trading  # Trading smoke tests only
make test-smoke-portfolio # Portfolio smoke tests only
make test-smoke-watchlist # Watchlist smoke tests only
make test-smoke-dashboard # Dashboard smoke tests only
make test-smoke-trades   # Trade history smoke tests only

# Utilities
make report              # Open HTML report
make clean               # Clean generated files
make clean-all           # Clean including venv
make help                # Show all commands
```

## Debugging Tips

```python
# Take screenshot
page_obj.take_screenshot('debug_screenshot')

# Add breakpoint
import pdb; pdb.set_trace()

# Print element text
print(page_obj.get_text('selector'))

# Check if element exists
if page_obj.is_visible('selector'):
    print("Element found!")

# Slow down execution
# In .env.test: SLOW_MO=500

# Run in headed mode
# In .env.test: HEADLESS=false
```

## Common Patterns

### Login Pattern
```python
login_page = LoginPage(page)
login_page.navigate()
login_page.login(TestData.PRIMARY_USER)
```

### Execute Trade Pattern
```python
trading_page = TradingPage(page)
trading_page.navigate()
trading_page.execute_buy_trade(quantity=10)
```

### Navigate Between Pages
```python
dashboard_page = DashboardPage(page)
dashboard_page.navigate_to_trading()  # Uses internal navigation
```

### Check and Act Pattern
```python
if portfolio_page.are_positions_displayed():
    portfolio_page.click_trade_button_for_position(0)
```

## Environment Variables (.env.test)

```bash
BASE_URL=http://localhost:5173
API_URL=http://localhost:5001/api
HEADLESS=true                # false to see browser
SLOW_MO=0                    # Milliseconds to slow down
TIMEOUT=30000                # Default timeout
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080
```

## Troubleshooting Quick Fixes

```bash
# Backend not running
cd backend && npm start

# Frontend not running
cd frontend && npm run dev

# Module not found
source venv/bin/activate    # Activate venv first

# Browsers not installed
make browsers

# Clean and retry
make clean && make setup
```

## Best Practices Checklist

- [ ] Use page objects, never direct selectors in tests
- [ ] Use TestData for all test data
- [ ] Add appropriate markers to tests
- [ ] Use descriptive test method names
- [ ] One test = one assertion/validation
- [ ] Clean up after tests (fixtures handle this)
- [ ] Take screenshots on failures (automatic)
- [ ] Use authenticated_page for protected pages

---

**Quick Reference v2.0** | [Full Documentation](README.md) | [Setup Guide](SETUP.md)
