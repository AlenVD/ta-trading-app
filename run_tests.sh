#!/bin/bash

# Test execution script for fintech trading app

set -e

echo "========================================="
echo "Fintech Trading App - UI Test Suite"
echo "========================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed${NC}"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}Creating virtual environment...${NC}"
    python3 -m venv venv
fi

# Activate virtual environment
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies
echo -e "${GREEN}Installing dependencies...${NC}"
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Install playwright browsers
echo -e "${GREEN}Installing Playwright browsers...${NC}"
playwright install chromium

# Create reports directory
mkdir -p reports/screenshots

# Check if backend is running
echo -e "${GREEN}Checking if backend is running...${NC}"
if ! curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
    echo -e "${RED}Error: Backend is not running on port 5001${NC}"
    echo -e "${YELLOW}Please start the backend with: cd backend && npm start${NC}"
    exit 1
fi

# Check if frontend is running
echo -e "${GREEN}Checking if frontend is running...${NC}"
if ! curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo -e "${RED}Error: Frontend is not running on port 5173${NC}"
    echo -e "${YELLOW}Please start the frontend with: cd frontend && npm run dev${NC}"
    exit 1
fi

echo -e "${GREEN}Both backend and frontend are running!${NC}"
echo ""

# Parse command line arguments
TEST_TYPE="${1:-all}"

case $TEST_TYPE in
    smoke)
        echo -e "${GREEN}Running smoke tests...${NC}"
        pytest -m smoke --html=reports/smoke_report.html --self-contained-html
        ;;
    auth)
        echo -e "${GREEN}Running authentication tests...${NC}"
        pytest -m auth --html=reports/auth_report.html --self-contained-html
        ;;
    trading)
        echo -e "${GREEN}Running trading tests...${NC}"
        pytest -m trading --html=reports/trading_report.html --self-contained-html
        ;;
    portfolio)
        echo -e "${GREEN}Running portfolio tests...${NC}"
        pytest -m portfolio --html=reports/portfolio_report.html --self-contained-html
        ;;
    watchlist)
        echo -e "${GREEN}Running watchlist tests...${NC}"
        pytest -m watchlist --html=reports/watchlist_report.html --self-contained-html
        ;;
    dashboard)
        echo -e "${GREEN}Running dashboard tests...${NC}"
        pytest -m dashboard --html=reports/dashboard_report.html --self-contained-html
        ;;
    regression)
        echo -e "${GREEN}Running regression tests...${NC}"
        pytest -m regression --html=reports/regression_report.html --self-contained-html
        ;;
    parallel)
        echo -e "${GREEN}Running all tests in parallel...${NC}"
        pytest -n auto --html=reports/parallel_report.html --self-contained-html
        ;;
    all)
        echo -e "${GREEN}Running all tests...${NC}"
        pytest --html=reports/test_report.html --self-contained-html
        ;;
    *)
        echo -e "${RED}Invalid test type: $TEST_TYPE${NC}"
        echo -e "${YELLOW}Usage: ./run_tests.sh [smoke|auth|trading|portfolio|watchlist|dashboard|regression|parallel|all]${NC}"
        exit 1
        ;;
esac

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}=========================================${NC}"
    echo -e "${GREEN}All tests passed!${NC}"
    echo -e "${GREEN}=========================================${NC}"
    echo ""
    echo -e "Test report: ${GREEN}reports/${TEST_TYPE}_report.html${NC}"
else
    echo ""
    echo -e "${RED}=========================================${NC}"
    echo -e "${RED}Some tests failed!${NC}"
    echo -e "${RED}=========================================${NC}"
    echo ""
    echo -e "Test report: ${YELLOW}reports/${TEST_TYPE}_report.html${NC}"
    exit 1
fi
