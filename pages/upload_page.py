from playwright.sync_api import sync_playwright
import pytest
from pathlib import Path
import os

from pages.base_page import BasePage


class UploadPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.file_input_selector = 'input[type="file"]'
        self.upload_button_selector = 'button[type="submit"]'
        self.message_selector = '#results'
        self.error_message_selector = 'input[type="file"]'

    def upload_file(self, file_name: str) -> str:
        """Upload a file and handle the response."""
        data_path = self._get_file_path(file_name)
        try:
            self._set_file_input(str(data_path))
            self._click_upload_button()
            return self._get_response()
        except Exception as e:
            self._handle_upload_error(e)

    def _get_file_path(self, file_name: str) -> Path:
        """Get the absolute path to the test file."""
        data_path = Path(__file__).parent.parent / "data" / file_name
        if not data_path.exists():
            raise FileNotFoundError(f"Test file not found at: {data_path}")
        return data_path

    def _set_file_input(self, file_path: str):
        """Set the file input with the test file."""
        self.page.set_input_files(self.file_input_selector, file_path, timeout=60000)

    def _click_upload_button(self):
        """Click the upload button and wait for it to be visible."""
        self.page.wait_for_selector(self.upload_button_selector, timeout=60000, state="visible")
        self.click(self.upload_button_selector)

    def _get_response(self) -> str:
        """Get the response message after upload."""
        self.page.wait_for_selector(self.message_selector, timeout=60000, state="visible")
        return self.get_text(self.message_selector)

    def _handle_upload_error(self, error: Exception):
        """Handle upload errors."""
        raise
