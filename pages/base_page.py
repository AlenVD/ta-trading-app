"""Base page object with common functionality."""
from typing import Optional
from playwright.sync_api import Page, Locator, expect
from config.settings import settings
import re


class BasePage:
    """Base page object that all page objects inherit from."""

    def __init__(self, page: Page):
        """Initialize base page.

        Args:
            page: Playwright page instance
        """
        self.page = page
        self.settings = settings
        self.timeout = settings.timeout

    # Navigation methods
    def goto(self, url: str, wait_until: str = 'networkidle'):
        """Navigate to URL.

        Args:
            url: URL to navigate to
            wait_until: Wait condition (load, domcontentloaded, networkidle)
        """
        self.page.goto(url, wait_until=wait_until, timeout=self.timeout)

    def wait_for_url(self, url: str, timeout: Optional[int] = None):
        """Wait for page to navigate to specific URL.

        Args:
            url: Expected URL or pattern
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.page.wait_for_url(url, timeout=timeout)

    def get_current_url(self) -> str:
        """Get current page URL.

        Returns:
            Current page URL
        """
        return self.page.url

    # Element interaction methods
    def find_element(self, selector: str) -> Locator:
        """Find element by selector.

        Args:
            selector: CSS selector or text selector

        Returns:
            Playwright Locator
        """
        return self.page.locator(selector)

    def find_by_text(self, text: str, exact: bool = False) -> Locator:
        """Find element by text content.

        Args:
            text: Text to search for (can be regex with /pattern/)
            exact: Whether to match exactly

        Returns:
            Playwright Locator
        """
        return self.page.locator(f'text={text}')

    def find_by_role(self, role: str, **kwargs) -> Locator:
        """Find element by ARIA role.

        Args:
            role: ARIA role (button, link, textbox, etc.)
            **kwargs: Additional filters (name, checked, etc.)

        Returns:
            Playwright Locator
        """
        return self.page.get_by_role(role, **kwargs)

    def click(self, selector: str, timeout: Optional[int] = None):
        """Click element.

        Args:
            selector: Element selector
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.page.click(selector, timeout=timeout)

    def fill(self, selector: str, value: str, timeout: Optional[int] = None):
        """Fill input field.

        Args:
            selector: Input field selector
            value: Value to fill
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.page.fill(selector, value, timeout=timeout)

    def get_text(self, selector: str) -> Optional[str]:
        """Get text content from element.

        Args:
            selector: Element selector

        Returns:
            Text content or None
        """
        return self.page.locator(selector).text_content()

    def get_value(self, selector: str) -> str:
        """Get input value.

        Args:
            selector: Input selector

        Returns:
            Input value
        """
        return self.page.locator(selector).input_value()

    # Wait methods
    def wait_for_element(self, selector: str, state: str = 'visible', timeout: Optional[int] = None):
        """Wait for element to reach specific state.

        Args:
            selector: Element selector
            state: State to wait for (visible, hidden, attached, detached)
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.page.wait_for_selector(selector, state=state, timeout=timeout)

    def wait_for_timeout(self, timeout: int):
        """Wait for specified timeout.

        Args:
            timeout: Timeout in milliseconds
        """
        self.page.wait_for_timeout(timeout)

    def wait_for_load_state(self, state: str = 'networkidle', timeout: Optional[int] = None):
        """Wait for page load state.

        Args:
            state: Load state (load, domcontentloaded, networkidle)
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.timeout
        self.page.wait_for_load_state(state, timeout=timeout)

    # Validation methods
    def is_visible(self, selector: str) -> bool:
        """Check if element is visible.

        Args:
            selector: Element selector

        Returns:
            True if visible, False otherwise
        """
        return self.page.locator(selector).is_visible()

    def is_enabled(self, selector: str) -> bool:
        """Check if element is enabled.

        Args:
            selector: Element selector

        Returns:
            True if enabled, False otherwise
        """
        return self.page.locator(selector).is_enabled()

    def element_count(self, selector: str) -> int:
        """Count elements matching selector.

        Args:
            selector: Element selector

        Returns:
            Number of matching elements
        """
        return self.page.locator(selector).count()

    # Assertion helpers
    def expect_visible(self, selector: str, timeout: Optional[int] = None):
        """Assert element is visible.

        Args:
            selector: Element selector
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.timeout
        expect(self.page.locator(selector)).to_be_visible(timeout=timeout)

    def expect_hidden(self, selector: str, timeout: Optional[int] = None):
        """Assert element is hidden.

        Args:
            selector: Element selector
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.timeout
        expect(self.page.locator(selector)).to_be_hidden(timeout=timeout)

    def expect_text(self, selector: str, text: str, timeout: Optional[int] = None):
        """Assert element contains text.

        Args:
            selector: Element selector
            text: Expected text
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.timeout
        expect(self.page.locator(selector)).to_contain_text(text, timeout=timeout)

    def expect_url(self, url: str, timeout: Optional[int] = None):
        """Assert page URL matches pattern.

        Args:
            url: Expected URL or pattern
            timeout: Timeout in milliseconds
        """
        timeout = timeout or self.timeout
        expect(self.page).to_have_url(url, timeout=timeout)

    # Screenshot methods
    def take_screenshot(self, name: str, full_page: bool = False):
        """Take screenshot.

        Args:
            name: Screenshot filename
            full_page: Whether to capture full page
        """
        import os
        os.makedirs(self.settings.screenshot_dir, exist_ok=True)
        path = f"{self.settings.screenshot_dir}/{name}.png"
        self.page.screenshot(path=path, full_page=full_page)

    # Local storage methods
    def get_local_storage_item(self, key: str) -> Optional[str]:
        """Get item from local storage.

        Args:
            key: Storage key

        Returns:
            Storage value or None
        """
        return self.page.evaluate(f'localStorage.getItem("{key}")')

    def set_local_storage_item(self, key: str, value: str):
        """Set item in local storage.

        Args:
            key: Storage key
            value: Storage value
        """
        self.page.evaluate(f'localStorage.setItem("{key}", "{value}")')

    def clear_local_storage(self):
        """Clear all local storage."""
        self.page.evaluate('localStorage.clear()')

    # Utility methods
    def extract_number_from_text(self, text: str) -> float:
        """Extract number from text like '$1,234.56'.

        Args:
            text: Text containing number

        Returns:
            Extracted number
        """
        cleaned = re.sub(r'[^0-9.-]', '', text)
        return float(cleaned) if cleaned else 0.0

    def wait_for_api_response(self, url_pattern: str, timeout: Optional[int] = None):
        """Wait for specific API response.

        Args:
            url_pattern: URL pattern to match
            timeout: Timeout in milliseconds

        Returns:
            Response object
        """
        timeout = timeout or self.timeout
        with self.page.expect_response(url_pattern, timeout=timeout) as response_info:
            response = response_info.value
        return response
