from pathlib import Path

from pages.base_page import BasePage

PROJECT_DIR = Path(__file__).parent
CSV_FILE_PATH = PROJECT_DIR / "data"


class UploadPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Selectors for the file upload page
        self.file_input_selector = 'input[type="file"][name="file"]'
        self.upload_button_selector = 'button[type="submit"]'
        self.message_selector = '#results'
        self.error_message_selector = 'input[type="file"]'

    def upload_file(self, file_name: str) -> str:
        """Upload a file."""
        self.navigate("http://localhost:8000")
        file_path = str(CSV_FILE_PATH / file_name)
        self.page.set_input_files(self.file_input_selector, file_path)
        self.page.wait_for_selector(self.upload_button_selector)
        self.page.click(self.upload_button_selector)
        # Wait for the error message
        self.page.wait_for_selector(self.message_selector)
        results = self.page.text_content(self.message_selector)
        return results

    def click_upload(self):
        """Click the upload button."""
        self.page.click(self.upload_button_selector)

    def get_success_message(self) -> str:
        """Retrieve the success message."""
        return self.get_text(self.message_selector)

    def get_error_message(self) -> str:
        """Retrieve the error message."""
        return self.get_text(self.error_message_selector)
