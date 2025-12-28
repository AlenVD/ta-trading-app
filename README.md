# Trading App - Test Automation Framework

A modern, OOP-based test automation framework for the Trading Application using **Page Object Model**, Python, pytest, and Playwright.

## Framework Architecture

This framework follows industry best practices with a clean OOP architecture:

```
ta-trading-app/
├── Makefile                    # Test execution commands
├── pytest.ini                  # Pytest configuration
├── requirements.txt            # Python dependencies
├── conftest.py                 # Pytest fixtures using POM
├── config/                     # Configuration management
│   ├── settings.py            # Centralized settings
│   └── test_data.py           # Test data management
├── models/                     # Data models
│   ├── user.py                # User model
│   ├── trade.py               # Trade model
│   └── stock.py               # Stock model
├── pages/                      # Page Object Model
│   ├── base_page.py           # Base page class
│   ├── login_page.py          # Login page object
│   ├── dashboard_page.py      # Dashboard page object
│   ├── trading_page.py        # Trading page object
│   ├── portfolio_page.py      # Portfolio page object
│   ├── watchlist_page.py      # Watchlist page object
│   └── trade_history_page.py  # Trade history page object
├── tests/                      # Test modules
│   ├── test_auth.py           # Authentication tests
│   ├── test_dashboard.py      # Dashboard tests
│   ├── test_trading.py        # Trading tests
│   ├── test_portfolio.py      # Portfolio tests
│   ├── test_watchlists.py     # Watchlist tests
│   └── test_trade_history.py  # Trade history tests
└── utils/                      # Utility functions
    └── helpers.py             # Helper functions
```

## Key Features

### 1. **Page Object Model (POM)**
- Clean separation between test logic and page interactions
- Reusable page objects with well-defined methods
- Centralized element locators
- Easy maintenance and scalability

### 2. **OOP Architecture**
- Base page class with common functionality
- Inheritance for code reuse
- Data models for type safety
- Configuration management classes

### 3. **Centralized Configuration**
- Settings loaded from environment variables
- Test data management in one place
- No hardcoded values in tests

### 4. **Make-based Test Execution**
- Simple, cross-platform commands
- No shell script dependencies
- Easy to extend and customize

### 5. **Comprehensive Test Coverage**
- Authentication & Authorization
- Trading functionality
- Portfolio management
- Watchlists
- Trade history
- Dashboard metrics

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for running the application)
- Make (comes with Linux/Mac, use Git Bash on Windows)

### Setup

1. **Install dependencies and browsers:**
```bash
make setup
```

This will:
- Create a virtual environment
- Install Python packages
- Install Playwright browsers

### Running Tests

Start the application first:
```bash
# Terminal 1 - Backend
cd backend && npm install && npm start

# Terminal 2 - Frontend  
cd frontend && npm install && npm run dev
```

Then run tests:

```bash
# Show all available commands
make help

# Run all tests
make test

# Run smoke tests (quick validation)
make test-smoke

# Run specific test suites
make test-auth          # Authentication tests
make test-trading       # Trading tests
make test-portfolio     # Portfolio tests
make test-watchlist     # Watchlist tests
make test-dashboard     # Dashboard tests
make test-trades        # Trade history tests

# Run tests in parallel (faster)
make test-parallel

# Run regression suite
make test-regression
```

### Test Reports

After running tests, HTML reports are generated in the `reports/` directory:

```bash
# Open latest test report
make report
```

Or manually open: `reports/test_report.html`

## Writing Tests with Page Object Model

### Example Test

```python
"""Example test using Page Object Model."""
import pytest
from playwright.sync_api import Page
from pages import LoginPage, DashboardPage
from config import TestData


@pytest.mark.smoke
class TestLogin:
    """Test login functionality."""

    def test_successful_login(self, page: Page):
        """Test user can login successfully."""
        # Initialize page objects
        login_page = LoginPage(page)
        dashboard_page = DashboardPage(page)

        # Navigate to login page
        login_page.navigate()

        # Perform login using test data
        login_page.login(TestData.PRIMARY_USER)

        # Verify login successful
        dashboard_page.expect_logged_in()
```

### Benefits of This Approach

**Before (Without POM):**
```python
# Hardcoded selectors and logic scattered everywhere
page.goto('/login')
page.fill('input[type="email"]', 'john@example.com')
page.fill('input[type="password"]', 'password123')
page.click('button[type="submit"]')
page.wait_for_url('/dashboard')
expect(page.locator('text=Logout')).to_be_visible()
```

**After (With POM):**
```python
# Clean, readable, maintainable
login_page.navigate()
login_page.login(TestData.PRIMARY_USER)
dashboard_page.expect_logged_in()
```

## Configuration

### Environment Variables

Create a `.env.test` file:

```bash
BASE_URL=http://localhost:5173
API_URL=http://localhost:5001/api
HEADLESS=true
SLOW_MO=0
TIMEOUT=30000
VIEWPORT_WIDTH=1920
VIEWPORT_HEIGHT=1080
```

### Test Data

Test data is centrally managed in `config/test_data.py`:

```python
from config import TestData

# Use predefined test users
user = TestData.PRIMARY_USER
users = TestData.get_all_users()

# Use predefined trade quantities
quantity = TestData.DEFAULT_TRADE_QUANTITY
```

## Page Objects

### Creating a New Page Object

```python
"""Example page object."""
from playwright.sync_api import Page
from .base_page import BasePage


class ExamplePage(BasePage):
    """Example page object."""

    # Locators as constants
    HEADER = 'h1'
    BUTTON = 'button.primary'

    def __init__(self, page: Page):
        super().__init__(page)
        self.url = self.settings.base_url + '/example'

    def navigate(self):
        """Navigate to example page."""
        self.goto(self.url)

    def click_button(self):
        """Click the primary button."""
        self.click(self.BUTTON)

    def expect_page_loaded(self):
        """Assert page is loaded."""
        self.expect_visible(self.HEADER)
```

## Test Markers

Tests are organized using pytest markers:

- `@pytest.mark.smoke` - Quick smoke tests
- `@pytest.mark.auth` - Authentication tests
- `@pytest.mark.trading` - Trading functionality
- `@pytest.mark.portfolio` - Portfolio tests
- `@pytest.mark.watchlist` - Watchlist tests
- `@pytest.mark.dashboard` - Dashboard tests
- `@pytest.mark.trades` - Trade history tests
- `@pytest.mark.regression` - Full regression suite

## Maintenance

### Clean Generated Files

```bash
# Clean reports and cache
make clean

# Clean everything including venv
make clean-all
```

### Update Dependencies

```bash
# Activate virtual environment
source venv/bin/activate

# Update packages
pip install --upgrade -r requirements.txt

# Install browsers
playwright install chromium
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Test Automation

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Setup
        run: make setup
      - name: Start Application
        run: |
          cd backend && npm install && npm start &
          cd frontend && npm install && npm run dev &
      - name: Run Tests
        run: make test-smoke
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: test-report
          path: reports/
```

## Best Practices

1. **Always use Page Objects** - Never interact with elements directly in tests
2. **Centralize test data** - Use `TestData` class for all test data
3. **Keep selectors in page objects** - As class constants
4. **Use descriptive method names** - Make tests self-documenting
5. **One assertion per test** - Keep tests focused
6. **Clean up after tests** - Use fixtures for setup/teardown
7. **Run smoke tests first** - Quick validation before full suite

## Troubleshooting

### Tests failing with "Backend not running"
```bash
cd backend && npm start
```

### Tests failing with "Frontend not running"
```bash
cd frontend && npm run dev
```

### Browser launch issues
```bash
make browsers  # Reinstall browsers
```

### Import errors
```bash
make clean
make setup
```

## Framework Advantages

### vs Shell Scripts
- ✅ Cross-platform (Windows, Linux, Mac)
- ✅ Better error handling
- ✅ Easier to maintain
- ✅ More readable

### vs Hardcoded Tests
- ✅ Reusable components
- ✅ Easy to maintain
- ✅ Less code duplication
- ✅ Better organization

### vs Procedural Code
- ✅ Object-oriented design
- ✅ Type safety with data models
- ✅ Clear abstractions
- ✅ Scalable architecture

## Contributing

When adding new tests:

1. Create/update page objects in `pages/`
2. Add test data to `config/test_data.py`
3. Write tests in `tests/` using page objects
4. Add appropriate markers
5. Update documentation

## Support

For issues or questions:
- Check the documentation in this README
- Review existing page objects for examples
- Run `make help` for available commands

---

**Framework Version:** 2.0 (OOP Refactored)  
**Last Updated:** 2025-12-28  
**Maintained by:** Test Architect Team
