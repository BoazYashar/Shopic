from playwright.sync_api import sync_playwright
import pytest
from pathlib import Path
import os


class UploadPage:
    def __init__(self, page):
        self.page = page
        self.file_input_selector = 'input[type="file"]'
        self.upload_button_selector = 'button[type="submit"]'
        self.message_selector = '#results'

    def navigate(self, url: str):
        """Navigate to the specified URL."""
        self.page.goto(url, timeout=60000)  # Increased timeout to 60 seconds

    def upload_file(self, file_name: str) -> str:
        """Upload a file and return the response."""
        # Get the absolute path to the test data directory
        current_dir = Path(__file__).parent
        project_root = current_dir.parent  # Go up one level
        data_path = project_root / "test_data" / file_name  # Assuming test_data directory

        # Ensure the file exists
        if not data_path.exists():
            raise FileNotFoundError(f"Test file not found at: {data_path}")

        print(f"Attempting to upload file from: {data_path}")

        try:
            # Set the file input with increased timeout
            self.page.set_input_files(
                self.file_input_selector,
                str(data_path),
                timeout=60000
            )

            # Wait for and click the upload button
            self.page.wait_for_selector(
                self.upload_button_selector,
                timeout=60000,
                state="visible"
            )
            self.page.click(self.upload_button_selector)

            # Wait for and get response
            self.page.wait_for_selector(
                self.message_selector,
                timeout=60000,
                state="visible"
            )
            return self.page.text_content(self.message_selector)

        except Exception as e:
            print(f"Error during file upload: {str(e)}")
            print(f"Current page URL: {self.page.url}")
            print(f"Page content: {self.page.content()}")
            raise