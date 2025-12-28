# Quick Setup Guide

Get started with the Trading App Test Automation Framework in minutes.

## Prerequisites

- **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
- **Node.js 16+**: Download from [nodejs.org](https://nodejs.org/)
- **Make**: 
  - Linux/Mac: Pre-installed
  - Windows: Use Git Bash or install GNU Make

## One-Command Setup

```bash
make setup
```

This command:
1. Creates a Python virtual environment
2. Installs all dependencies
3. Installs Playwright browsers (Chromium)
4. Creates report directories

## Manual Setup (If make is not available)

### 1. Create Virtual Environment

```bash
python3 -m venv venv
```

### 2. Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows (Git Bash):**
```bash
source venv/Scripts/activate
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Install Playwright Browsers

```bash
playwright install chromium
```

### 5. Create Report Directories

```bash
mkdir -p reports/screenshots
```

## Starting the Application

The tests require the application to be running.

### Terminal 1 - Start Backend

```bash
cd backend
npm install
npm start
```

Backend will run on: `http://localhost:5001`

### Terminal 2 - Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend will run on: `http://localhost:5173`

## Running Your First Test

### Terminal 3 - Run Tests

```bash
# Run smoke tests (quickest validation)
make test-smoke

# Or without make:
source venv/bin/activate
pytest tests -m smoke --html=reports/smoke_report.html --self-contained-html
```

If tests pass, you'll see:
```
======================== X passed in Xs ========================
```

## Configuration

### Environment Variables (Optional)

Create `.env.test` file in the project root:

```bash
BASE_URL=http://localhost:5173
API_URL=http://localhost:5001/api
HEADLESS=true
SLOW_MO=0
TIMEOUT=30000
```

### Browser Settings

- **Headless mode**: Set `HEADLESS=false` to see browser
- **Slow motion**: Set `SLOW_MO=500` to slow down actions (ms)
- **Timeout**: Set `TIMEOUT=60000` for slower systems (ms)

## All Available Commands

```bash
make help              # Show all commands
make setup             # Full setup
make test              # Run all tests
make test-smoke        # Run smoke tests
make test-auth         # Run authentication tests
make test-trading      # Run trading tests
make test-portfolio    # Run portfolio tests
make test-watchlist    # Run watchlist tests
make test-dashboard    # Run dashboard tests
make test-trades       # Run trade history tests
make test-parallel     # Run tests in parallel
make report            # Open latest HTML report
make clean             # Clean generated files
```

## Verification

After setup, verify everything works:

```bash
# Check Python version
python3 --version

# Check pytest
source venv/bin/activate
pytest --version

# Check playwright
playwright --version

# Run smoke tests
make test-smoke
```

## Troubleshooting

### "make: command not found"

**Solution**: Use manual setup commands or install make:
- Windows: Install via Git Bash or Chocolatey (`choco install make`)
- Mac: `xcode-select --install`

### "Backend is not running"

**Solution**: Start backend first:
```bash
cd backend && npm start
```

### "Frontend is not running"

**Solution**: Start frontend:
```bash
cd frontend && npm run dev
```

### "ModuleNotFoundError"

**Solution**: Activate virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows
```

### "Playwright browsers not found"

**Solution**: Install browsers:
```bash
playwright install chromium
```

### Port conflicts (5001 or 5173 already in use)

**Solution 1**: Stop other services using these ports

**Solution 2**: Update `.env.test` with different ports:
```bash
BASE_URL=http://localhost:3000
API_URL=http://localhost:8000/api
```

### Tests failing randomly

**Solution**: Increase timeout in `.env.test`:
```bash
TIMEOUT=60000
SLOW_MO=100
```

### Permission denied errors

**Solution**: Fix permissions:
```bash
chmod +x venv/bin/*
```

## Project Structure

After setup, your directory will look like:

```
ta-trading-app/
├── venv/                   # Virtual environment (created by setup)
├── reports/                # Test reports (created by setup)
│   └── screenshots/        # Failure screenshots
├── config/                 # Configuration classes
├── models/                 # Data models
├── pages/                  # Page objects
├── tests/                  # Test modules
├── utils/                  # Helper functions
├── Makefile               # Test commands
├── pytest.ini             # Pytest config
└── requirements.txt       # Dependencies
```

## Next Steps

1. ✅ Complete setup
2. ✅ Start application (backend + frontend)
3. ✅ Run smoke tests
4. 📖 Read [README.md](README.md) for detailed documentation
5. 🧪 Write your first test using Page Objects

## Quick Reference

### Daily Workflow

```bash
# 1. Start application (in separate terminals)
cd backend && npm start
cd frontend && npm run dev

# 2. Activate virtual environment
source venv/bin/activate

# 3. Run tests
make test-smoke          # Quick validation
make test                # Full suite
make test-auth           # Specific module

# 4. View results
make report              # Open HTML report
```

### Updating Framework

```bash
# Pull latest changes
git pull

# Reinstall dependencies
make clean
make setup

# Run tests to verify
make test-smoke
```

## Getting Help

1. Run `make help` for available commands
2. Check [README.md](README.md) for detailed documentation
3. Review test examples in `tests/` directory
4. Examine page objects in `pages/` directory

---

**Happy Testing! 🚀**
