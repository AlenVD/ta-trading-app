# ReportPortal Launch Names Reference

This document shows all the dynamic ReportPortal launch names used by each Make command.

## Overview

Each test command now sets a unique ReportPortal launch name, making it easy to identify which test suite was run in ReportPortal.

## Launch Name Mapping

### All Tests
| Command | RP Launch Name | Description |
|---------|---------------|-------------|
| `make test` | `trading-app-all-tests` | All tests execution |
| `make test-smoke` | `trading-app-smoke` | Smoke tests - Quick validation |
| `make test-parallel` | `trading-app-parallel` | All tests - Parallel execution |
| `make test-regression` | `trading-app-regression` | Regression test suite |

### Module-Specific Tests (All Tests)
| Command | RP Launch Name | Description |
|---------|---------------|-------------|
| `make test-auth` | `trading-app-auth` | Authentication module - All tests |
| `make test-trading` | `trading-app-trading` | Trading module - All tests |
| `make test-portfolio` | `trading-app-portfolio` | Portfolio module - All tests |
| `make test-watchlist` | `trading-app-watchlist` | Watchlist module - All tests |
| `make test-dashboard` | `trading-app-dashboard` | Dashboard module - All tests |
| `make test-trades` | `trading-app-trades` | Trade history module - All tests |

### Module-Specific Smoke Tests
| Command | RP Launch Name | Description |
|---------|---------------|-------------|
| `make test-smoke-auth` | `trading-app-smoke-auth` | Auth module smoke tests |
| `make test-smoke-trading` | `trading-app-smoke-trading` | Trading module smoke tests |
| `make test-smoke-portfolio` | `trading-app-smoke-portfolio` | Portfolio module smoke tests |
| `make test-smoke-watchlist` | `trading-app-smoke-watchlist` | Watchlist module smoke tests |
| `make test-smoke-dashboard` | `trading-app-smoke-dashboard` | Dashboard module smoke tests |
| `make test-smoke-trades` | `trading-app-smoke-trades` | Trade history module smoke tests |

## How It Works

The launch name is set dynamically using environment variables in the Makefile:

```makefile
test-smoke-auth: pre-test
	@RP_LAUNCH="trading-app-smoke-auth" RP_LAUNCH_DESCRIPTION="Auth module smoke tests" \
		$(PYTEST) $(TEST_DIR) -m "smoke and auth" --html=$(REPORT_DIR)/smoke_auth_report.html
```

ReportPortal will pick up the `RP_LAUNCH` and `RP_LAUNCH_DESCRIPTION` environment variables automatically.

## Configuration

The base ReportPortal configuration is in [pytest.ini](pytest.ini):

```ini
rp_endpoint = http://localhost:8080
rp_project = trading-fintech-app
rp_api_key = trading-fintech-app_BsEUW0hrTTGASpaI7UBfs9tlQ4xUz7fMnil5EAc3u1Kg5No-4f9aXW8p1DSU--f2
rp_launch_attributes = 'env:sit'
```

The `rp_launch` is intentionally NOT set in pytest.ini - it's set dynamically by each Make command.

## Benefits

✅ **Easy Identification**: Each launch has a clear, descriptive name
✅ **Organized Reports**: Filter by module (auth, trading, etc.) or test type (smoke, all, regression)
✅ **No Manual Updates**: Launch name changes automatically based on command
✅ **Consistent Naming**: All names follow `trading-app-{type}-{module}` pattern

## Examples

### In ReportPortal, you'll see launches like:

- `trading-app-smoke` - From running `make test-smoke`
- `trading-app-smoke-auth` - From running `make test-smoke-auth`
- `trading-app-auth` - From running `make test-auth`
- `trading-app-parallel` - From running `make test-parallel`

This makes it very easy to find the exact test run you're looking for!

## Overriding in CI/CD

You can override the launch name in CI/CD by setting environment variables:

```bash
# In Jenkins/GitHub Actions
export RP_LAUNCH="trading-app-ci-build-${BUILD_NUMBER}"
export RP_LAUNCH_DESCRIPTION="CI Build #${BUILD_NUMBER} - Smoke Tests"
make test-smoke
```

The CI environment variables will override the Makefile defaults.

---

**Last Updated**: 2025-12-28
