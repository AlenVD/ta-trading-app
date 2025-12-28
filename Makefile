.PHONY: help install setup browsers clean test test-smoke test-smoke-auth test-smoke-trading test-smoke-portfolio test-smoke-watchlist test-smoke-dashboard test-smoke-trades test-auth test-trading test-portfolio test-watchlist test-dashboard test-trades test-regression test-parallel test-all report

# Colors for terminal output
GREEN  := \033[0;32m
YELLOW := \033[1;33m
RED    := \033[0;31m
NC     := \033[0m # No Color

# Configuration
PYTHON := python3
VENV := venv
VENV_BIN := $(VENV)/bin
PIP := $(VENV_BIN)/pip
PYTEST := $(VENV_BIN)/pytest
PLAYWRIGHT := $(VENV_BIN)/playwright
REPORT_DIR := reports
TEST_DIR := tests

# Help target
help:
	@echo "$(GREEN)=========================================$(NC)"
	@echo "$(GREEN)Trading App - Test Framework$(NC)"
	@echo "$(GREEN)=========================================$(NC)"
	@echo ""
	@echo "$(YELLOW)Available targets:$(NC)"
	@echo "  $(GREEN)make install$(NC)             - Install dependencies and setup environment"
	@echo "  $(GREEN)make setup$(NC)               - Full setup (install + browsers)"
	@echo "  $(GREEN)make browsers$(NC)            - Install Playwright browsers"
	@echo ""
	@echo "$(YELLOW)All Tests:$(NC)"
	@echo "  $(GREEN)make test$(NC)                - Run all tests"
	@echo "  $(GREEN)make test-smoke$(NC)          - Run all smoke tests"
	@echo "  $(GREEN)make test-parallel$(NC)       - Run all tests in parallel"
	@echo "  $(GREEN)make test-regression$(NC)     - Run regression tests"
	@echo ""
	@echo "$(YELLOW)Module-Specific Tests:$(NC)"
	@echo "  $(GREEN)make test-auth$(NC)           - Run all authentication tests"
	@echo "  $(GREEN)make test-trading$(NC)        - Run all trading tests"
	@echo "  $(GREEN)make test-portfolio$(NC)      - Run all portfolio tests"
	@echo "  $(GREEN)make test-watchlist$(NC)      - Run all watchlist tests"
	@echo "  $(GREEN)make test-dashboard$(NC)      - Run all dashboard tests"
	@echo "  $(GREEN)make test-trades$(NC)         - Run all trade history tests"
	@echo ""
	@echo "$(YELLOW)Module-Specific Smoke Tests:$(NC)"
	@echo "  $(GREEN)make test-smoke-auth$(NC)     - Run auth smoke tests only"
	@echo "  $(GREEN)make test-smoke-trading$(NC)  - Run trading smoke tests only"
	@echo "  $(GREEN)make test-smoke-portfolio$(NC)- Run portfolio smoke tests only"
	@echo "  $(GREEN)make test-smoke-watchlist$(NC)- Run watchlist smoke tests only"
	@echo "  $(GREEN)make test-smoke-dashboard$(NC)- Run dashboard smoke tests only"
	@echo "  $(GREEN)make test-smoke-trades$(NC)   - Run trade history smoke tests only"
	@echo ""
	@echo "$(YELLOW)Utilities:$(NC)"
	@echo "  $(GREEN)make report$(NC)              - Open latest HTML test report"
	@echo "  $(GREEN)make clean$(NC)               - Clean generated files"
	@echo ""

# Check if Python is installed
check-python:
	@which $(PYTHON) > /dev/null || (echo "$(RED)Error: Python 3 is not installed$(NC)" && exit 1)

# Create virtual environment
$(VENV):
	@echo "$(GREEN)Creating virtual environment...$(NC)"
	@$(PYTHON) -m venv $(VENV)

# Install dependencies
install: check-python $(VENV)
	@echo "$(GREEN)Installing dependencies...$(NC)"
	@$(PIP) install --upgrade pip > /dev/null
	@$(PIP) install -r requirements.txt

# Install Playwright browsers
browsers: install
	@echo "$(GREEN)Installing Playwright browsers...$(NC)"
	@$(PLAYWRIGHT) install chromium

# Full setup
setup: install browsers
	@echo "$(GREEN)Setup complete!$(NC)"
	@mkdir -p $(REPORT_DIR)/screenshots

# Check if backend is running
check-backend:
	@echo "$(GREEN)Checking if backend is running...$(NC)"
	@curl -s http://localhost:5001/api/health > /dev/null 2>&1 || \
		(echo "$(RED)Error: Backend is not running on port 5001$(NC)" && \
		 echo "$(YELLOW)Please start the backend with: cd backend && npm start$(NC)" && \
		 exit 1)

# Check if frontend is running
check-frontend:
	@echo "$(GREEN)Checking if frontend is running...$(NC)"
	@curl -s http://localhost:5173 > /dev/null 2>&1 || \
		(echo "$(RED)Error: Frontend is not running on port 5173$(NC)" && \
		 echo "$(YELLOW)Please start the frontend with: cd frontend && npm run dev$(NC)" && \
		 exit 1)

# Pre-test checks
pre-test: check-backend check-frontend
	@echo "$(GREEN)Both backend and frontend are running!$(NC)"
	@mkdir -p $(REPORT_DIR)/screenshots

# Run all tests
test: pre-test
	@echo "$(GREEN)Running all tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) \
		--rp-launch="trading-app-all-tests" \
		--rp-launch-description="All tests execution" \
		--html=$(REPORT_DIR)/test_report.html --self-contained-html || \
		(echo "$(RED)Some tests failed!$(NC)" && exit 1)
	@echo "$(GREEN)All tests passed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/test_report.html$(NC)"

# Run all tests (alias)
test-all: test

# Run smoke tests
test-smoke: pre-test
	@echo "$(GREEN)Running smoke tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m smoke \
		--rp-launch="trading-app-smoke" \
		--rp-launch-description="Smoke tests - Quick validation" \
		--html=$(REPORT_DIR)/smoke_report.html --self-contained-html
	@echo "$(GREEN)Smoke tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/smoke_report.html$(NC)"

# Run module-specific smoke tests
test-smoke-auth: pre-test
	@echo "$(GREEN)Running auth smoke tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m "smoke and auth" \
		--rp-launch="trading-app-smoke-auth" \
		--rp-launch-description="Auth module smoke tests" \
		--html=$(REPORT_DIR)/smoke_auth_report.html --self-contained-html
	@echo "$(GREEN)Auth smoke tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/smoke_auth_report.html$(NC)"

test-smoke-trading: pre-test
	@echo "$(GREEN)Running trading smoke tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m "smoke and trading" \
		--rp-launch="trading-app-smoke-trading" \
		--rp-launch-description="Trading module smoke tests" \
		--html=$(REPORT_DIR)/smoke_trading_report.html --self-contained-html
	@echo "$(GREEN)Trading smoke tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/smoke_trading_report.html$(NC)"

test-smoke-portfolio: pre-test
	@echo "$(GREEN)Running portfolio smoke tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m "smoke and portfolio" \
		--rp-launch="trading-app-smoke-portfolio" \
		--rp-launch-description="Portfolio module smoke tests" \
		--html=$(REPORT_DIR)/smoke_portfolio_report.html --self-contained-html
	@echo "$(GREEN)Portfolio smoke tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/smoke_portfolio_report.html$(NC)"

test-smoke-watchlist: pre-test
	@echo "$(GREEN)Running watchlist smoke tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m "smoke and watchlist" \
		--rp-launch="trading-app-smoke-watchlist" \
		--rp-launch-description="Watchlist module smoke tests" \
		--html=$(REPORT_DIR)/smoke_watchlist_report.html --self-contained-html
	@echo "$(GREEN)Watchlist smoke tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/smoke_watchlist_report.html$(NC)"

test-smoke-dashboard: pre-test
	@echo "$(GREEN)Running dashboard smoke tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m "smoke and dashboard" \
		--rp-launch="trading-app-smoke-dashboard" \
		--rp-launch-description="Dashboard module smoke tests" \
		--html=$(REPORT_DIR)/smoke_dashboard_report.html --self-contained-html
	@echo "$(GREEN)Dashboard smoke tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/smoke_dashboard_report.html$(NC)"

test-smoke-trades: pre-test
	@echo "$(GREEN)Running trade history smoke tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m "smoke and trades" \
		--rp-launch="trading-app-smoke-trades" \
		--rp-launch-description="Trade history module smoke tests" \
		--html=$(REPORT_DIR)/smoke_trades_report.html --self-contained-html
	@echo "$(GREEN)Trade history smoke tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/smoke_trades_report.html$(NC)"

# Run authentication tests
test-auth: pre-test
	@echo "$(GREEN)Running authentication tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m auth \
		--rp-launch="trading-app-auth" \
		--rp-launch-description="Authentication module - All tests" \
		--html=$(REPORT_DIR)/auth_report.html --self-contained-html
	@echo "$(GREEN)Authentication tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/auth_report.html$(NC)"

# Run trading tests
test-trading: pre-test
	@echo "$(GREEN)Running trading tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m trading \
		--rp-launch="trading-app-trading" \
		--rp-launch-description="Trading module - All tests" \
		--html=$(REPORT_DIR)/trading_report.html --self-contained-html
	@echo "$(GREEN)Trading tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/trading_report.html$(NC)"

# Run portfolio tests
test-portfolio: pre-test
	@echo "$(GREEN)Running portfolio tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m portfolio \
		--rp-launch="trading-app-portfolio" \
		--rp-launch-description="Portfolio module - All tests" \
		--html=$(REPORT_DIR)/portfolio_report.html --self-contained-html
	@echo "$(GREEN)Portfolio tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/portfolio_report.html$(NC)"

# Run watchlist tests
test-watchlist: pre-test
	@echo "$(GREEN)Running watchlist tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m watchlist \
		--rp-launch="trading-app-watchlist" \
		--rp-launch-description="Watchlist module - All tests" \
		--html=$(REPORT_DIR)/watchlist_report.html --self-contained-html
	@echo "$(GREEN)Watchlist tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/watchlist_report.html$(NC)"

# Run dashboard tests
test-dashboard: pre-test
	@echo "$(GREEN)Running dashboard tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m dashboard \
		--rp-launch="trading-app-dashboard" \
		--rp-launch-description="Dashboard module - All tests" \
		--html=$(REPORT_DIR)/dashboard_report.html --self-contained-html
	@echo "$(GREEN)Dashboard tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/dashboard_report.html$(NC)"

# Run trade history tests
test-trades: pre-test
	@echo "$(GREEN)Running trade history tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m trades \
		--rp-launch="trading-app-trades" \
		--rp-launch-description="Trade history module - All tests" \
		--html=$(REPORT_DIR)/trades_report.html --self-contained-html
	@echo "$(GREEN)Trade history tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/trades_report.html$(NC)"

# Run regression tests
test-regression: pre-test
	@echo "$(GREEN)Running regression tests...$(NC)"
	@$(PYTEST) $(TEST_DIR) -m regression \
		--rp-launch="trading-app-regression" \
		--rp-launch-description="Regression test suite" \
		--html=$(REPORT_DIR)/regression_report.html --self-contained-html
	@echo "$(GREEN)Regression tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/regression_report.html$(NC)"

# Run tests in parallel
test-parallel: pre-test
	@echo "$(GREEN)Running tests in parallel...$(NC)"
	@$(PYTEST) $(TEST_DIR) -n auto \
		--rp-launch="trading-app-parallel" \
		--rp-launch-description="All tests - Parallel execution" \
		--html=$(REPORT_DIR)/parallel_report.html --self-contained-html
	@echo "$(GREEN)Parallel tests completed!$(NC)"
	@echo "$(GREEN)Report: $(REPORT_DIR)/parallel_report.html$(NC)"

# Open latest HTML report
report:
	@if [ -f $(REPORT_DIR)/test_report.html ]; then \
		echo "$(GREEN)Opening test report...$(NC)"; \
		xdg-open $(REPORT_DIR)/test_report.html 2>/dev/null || open $(REPORT_DIR)/test_report.html 2>/dev/null || echo "$(YELLOW)Please open $(REPORT_DIR)/test_report.html manually$(NC)"; \
	else \
		echo "$(RED)No test report found. Run tests first.$(NC)"; \
	fi

# Clean generated files
clean:
	@echo "$(YELLOW)Cleaning generated files...$(NC)"
	@rm -rf $(REPORT_DIR)/*.html
	@rm -rf $(REPORT_DIR)/screenshots/*
	@rm -rf .pytest_cache
	@rm -rf __pycache__
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)Clean complete!$(NC)"

# Clean everything including venv
clean-all: clean
	@echo "$(YELLOW)Removing virtual environment...$(NC)"
	@rm -rf $(VENV)
	@echo "$(GREEN)Clean all complete!$(NC)"
