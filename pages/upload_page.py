from pages.base_page import BasePage


class UploadPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Selectors for the file upload page
        self.file_input_selector = 'input[type="file"][name="file"]'
        self.upload_button_selector = 'button[type="submit"]'
        self.message_selector = '#results'
        self.error_message_selector = 'input[type="file"]'

    def upload_file(self, file_path: str):
        """Upload a file."""
        self.page.set_input_files(self.file_input_selector, file_path)

    def click_upload(self):
        """Click the upload button."""
        self.page.click(self.upload_button_selector)

    def get_success_message(self) -> str:
        """Retrieve the success message."""
        return self.get_text(self.message_selector)

    def get_error_message(self) -> str:
        """Retrieve the error message."""
        return self.get_text(self.error_message_selector)
