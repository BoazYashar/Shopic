import json
from pathlib import Path

import pytest
from playwright.sync_api import sync_playwright

from pages.upload_page import UploadPage


def test_response_format_and_values():
    """Test that the server response has the correct format and values."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        upload_page = UploadPage(page)

        # Upload a valid file and click on upload
        response = upload_page.upload_file("valid_products.csv")

        # parse it as JSON
        parsed_response = json.loads(response)

        # Validate the top-level keys
        assert "status" in parsed_response, "Missing 'status' key in response"
        assert "data" in parsed_response, "Missing 'data' key in response"

        # Validate the status value
        assert parsed_response["status"] == "success", f"Unexpected status: {parsed_response['status']}"

        # Validate the structure of the 'data' array
        assert isinstance(parsed_response["data"], list), "'data' is not a list"
        assert len(parsed_response["data"]) > 0, "'data' array is empty"

        # Validate the first item in 'data'
        first_item = parsed_response["data"][0]
        expected_keys = {"id", "name", "price", "category", "stock"}
        assert expected_keys.issubset(
            first_item.keys()), f"Missing keys in 'data[0]': {expected_keys - set(first_item.keys())}"

        # Validate specific values in the first item
        assert first_item["id"] == 1, f"Unexpected id: {first_item['id']}"
        assert first_item["name"] == "Laptop", f"Unexpected name: {first_item['name']}"
        assert first_item["price"] == 999.99, f"Unexpected price: {first_item['price']}"
        assert first_item["category"] == "Electronics", f"Unexpected category: {first_item['category']}"
        assert first_item["stock"] == 50, f"Unexpected stock: {first_item['stock']}"

        browser.close()


def test_invalid_upload():
    """Test uploading an invalid CSV file and verify the error message."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        upload_page = UploadPage(page)

        try:
            # Navigate to the upload page
            upload_page.navigate("http://localhost:8000")

            # Upload an invalid file
            results = upload_page.upload_file("invalid_products.csv")

            # Assert that the response contains 'error'
            assert "error" in results.lower(), f"Expected 'error' in results, but got: {results}"

        finally:
            browser.close()


def test_nameless_upload():
    """Test uploading a CSV file with missing names and verify the error message."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        upload_page = UploadPage(page)

        try:
            # Navigate to the upload page
            upload_page.navigate("http://localhost:8000")

            # Upload a file with missing names
            results = upload_page.upload_file("nameless_products.csv")

            # Assert that the error message contains the expected text
            expected_error = "Missing name in row"
            assert expected_error in results, f"Expected '{expected_error}' in results, but got: {results}"

        finally:
            browser.close()


def test_empty_file_upload():
    """Test uploading an empty CSV file and verify the error message."""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        upload_page = UploadPage(page)

        try:
            # Navigate to the upload page
            upload_page.navigate("http://localhost:8000")

            # Upload an empty file
            results = upload_page.upload_file("empty.csv")

            # Assert that the error message contains the expected text
            expected_error = "No columns to parse from file"
            assert expected_error in results, f"Expected '{expected_error}' in results, but got: {results}"

        finally:
            browser.close()


from playwright.sync_api import sync_playwright


def test_no_file_selected():
    """
    Test clicking the upload button without selecting a file.
    The test checks whether a dialog or an inline error appears when the file input is empty.
    """
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        upload_page = UploadPage(page)

        try:
            # Navigate to the upload page
            page.goto("http://localhost:8000")

            # Variable to store the dialog message
            dialog_message = None

            # Define a handler for the dialog event
            def handle_dialog(dialog):
                nonlocal dialog_message
                dialog_message = dialog.message
                dialog.dismiss()

            page.on("dialog", handle_dialog)

            # Click the upload button without selecting a file
            upload_page.click_upload()

            # # Wait briefly to ensure the dialog has time to appear
            # page.wait_for_timeout(1000)

            if dialog_message:
                # If a dialog appears, verify its message
                expected_messages = ["Please select a file.", "יש לבחור קובץ."]
                assert dialog_message in expected_messages, f"Unexpected dialog message: {dialog_message}"
            else:
                # If no dialog appears, check for inline validation or error messages
                error_selector = "input:invalid"  # CSS selector for invalid input elements
                invalid_input = page.query_selector(error_selector)

                assert invalid_input is not None, "No error message or dialog was triggered."
                print("Validation error triggered successfully.")
        finally:
            browser.close()
