from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        """Initialize the BasePage with a Playwright Page object."""
        self.page = page

    def navigate(self, url: str):
        """Navigate to a specific URL."""
        self.page.goto(url)

    def get_text(self, selector: str) -> str:
        """Retrieve text content from an element based on the provided selector."""
        return self.page.text_content(selector)

    def click(self, selector: str):
        """Click on an element specified by the selector."""
        self.page.click(selector)
