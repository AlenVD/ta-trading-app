@echo off
REM Test execution script for fintech trading app (Windows)

echo =========================================
echo Fintech Trading App - UI Test Suite
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -q --upgrade pip
pip install -q -r requirements.txt

REM Install playwright browsers
echo Installing Playwright browsers...
playwright install chromium

REM Create reports directory
if not exist "reports\screenshots" mkdir reports\screenshots

REM Check if backend is running
echo Checking if backend is running...
curl -s http://localhost:5001/api/health >nul 2>&1
if errorlevel 1 (
    echo Error: Backend is not running on port 5001
    echo Please start the backend with: cd backend ^&^& npm start
    exit /b 1
)

REM Check if frontend is running
echo Checking if frontend is running...
curl -s http://localhost:5173 >nul 2>&1
if errorlevel 1 (
    echo Error: Frontend is not running on port 5173
    echo Please start the frontend with: cd frontend ^&^& npm run dev
    exit /b 1
)

echo Both backend and frontend are running!
echo.

REM Parse command line arguments
set TEST_TYPE=%1
if "%TEST_TYPE%"=="" set TEST_TYPE=all

if "%TEST_TYPE%"=="smoke" (
    echo Running smoke tests...
    pytest -m smoke --html=reports/smoke_report.html --self-contained-html
) else if "%TEST_TYPE%"=="auth" (
    echo Running authentication tests...
    pytest -m auth --html=reports/auth_report.html --self-contained-html
) else if "%TEST_TYPE%"=="trading" (
    echo Running trading tests...
    pytest -m trading --html=reports/trading_report.html --self-contained-html
) else if "%TEST_TYPE%"=="portfolio" (
    echo Running portfolio tests...
    pytest -m portfolio --html=reports/portfolio_report.html --self-contained-html
) else if "%TEST_TYPE%"=="watchlist" (
    echo Running watchlist tests...
    pytest -m watchlist --html=reports/watchlist_report.html --self-contained-html
) else if "%TEST_TYPE%"=="dashboard" (
    echo Running dashboard tests...
    pytest -m dashboard --html=reports/dashboard_report.html --self-contained-html
) else if "%TEST_TYPE%"=="regression" (
    echo Running regression tests...
    pytest -m regression --html=reports/regression_report.html --self-contained-html
) else if "%TEST_TYPE%"=="parallel" (
    echo Running all tests in parallel...
    pytest -n auto --html=reports/parallel_report.html --self-contained-html
) else if "%TEST_TYPE%"=="all" (
    echo Running all tests...
    pytest --html=reports/test_report.html --self-contained-html
) else (
    echo Invalid test type: %TEST_TYPE%
    echo Usage: run_tests.bat [smoke^|auth^|trading^|portfolio^|watchlist^|dashboard^|regression^|parallel^|all]
    exit /b 1
)

if errorlevel 1 (
    echo.
    echo =========================================
    echo Some tests failed!
    echo =========================================
    echo.
    echo Test report: reports\%TEST_TYPE%_report.html
    exit /b 1
) else (
    echo.
    echo =========================================
    echo All tests passed!
    echo =========================================
    echo.
    echo Test report: reports\%TEST_TYPE%_report.html
)
