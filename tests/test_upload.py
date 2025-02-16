import json
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from pages.upload_page import UploadPage


def test_file_upload_http2():
    """Test file upload with HTTP/2 support."""
    with sync_playwright() as p:
        browser = p.chromium.launch(
            args=['--enable-http2'],
            headless=False  # Make browser visible for debugging
        )

        context = browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            ignore_https_errors=True
        )

        page = context.new_page()
        upload_page = UploadPage(page)

        try:
            # Navigate and perform upload
            upload_page.navigate("http://localhost:8000")
            response = upload_page.upload_file(r"C:\Automation\Shopic\Shopic\data\valid_products.csv")

            # Verify response
            assert response is not None, "No response received"
            print(f"Upload response: {response}")

        except Exception as e:
            # Take screenshot on failure
            page.screenshot(path="error-screenshot.png")
            raise

        finally:
            browser.close()


def test_no_file_selected():
    """Test clicking upload without selecting a file."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        upload_page = UploadPage(page)

        try:
            upload_page.navigate("http://localhost:8000")
            page.click(upload_page.upload_button_selector)

            error_selector = "input:invalid"
            invalid_input = page.query_selector(error_selector)
            assert invalid_input is not None, "No validation error triggered"

        finally:
            browser.close()


if __name__ == "__main__":
    pytest.main([__file__])