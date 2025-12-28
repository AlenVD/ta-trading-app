"""Helper utilities for tests."""
from playwright.sync_api import Page, expect


def wait_for_url(page: Page, url: str, timeout: int = 30000):
    """Wait for page to navigate to specific URL."""
    page.wait_for_url(url, timeout=timeout)


def wait_for_element(page: Page, selector: str, timeout: int = 30000):
    """Wait for element to be visible."""
    page.wait_for_selector(selector, state='visible', timeout=timeout)


def fill_input(page: Page, selector: str, value: str):
    """Fill input field with value."""
    page.fill(selector, value)


def click_button(page: Page, selector: str):
    """Click button and wait for response."""
    page.click(selector)


def get_text(page: Page, selector: str) -> str:
    """Get text content from element."""
    return page.locator(selector).text_content()


def element_exists(page: Page, selector: str) -> bool:
    """Check if element exists on page."""
    return page.locator(selector).count() > 0


def wait_for_navigation(page: Page, timeout: int = 30000):
    """Wait for page navigation to complete."""
    page.wait_for_load_state('networkidle', timeout=timeout)


def take_screenshot(page: Page, name: str):
    """Take screenshot for debugging."""
    page.screenshot(path=f"reports/screenshots/{name}.png")


def extract_number_from_text(text: str) -> float:
    """Extract number from text like '$1,234.56' -> 1234.56"""
    import re
    cleaned = re.sub(r'[^0-9.-]', '', text)
    return float(cleaned) if cleaned else 0.0


def wait_for_api_response(page: Page, url_pattern: str, timeout: int = 30000):
    """Wait for specific API response."""
    with page.expect_response(url_pattern, timeout=timeout) as response_info:
        response = response_info.value
    return response
