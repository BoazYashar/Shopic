import json
from pathlib import Path
from typing import Generator

import pytest
from playwright.async_api import Page
from playwright.sync_api import sync_playwright

from pages.upload_page import UploadPage


@pytest.fixture(scope="function")
def browser_context() -> Generator[Page, None, None]:
    """Fixture to handle browser setup and teardown."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080}, ignore_https_errors=True)
        page = context.new_page()
        yield page
        browser.close()


def test_response_format_and_values(browser_context):
    """Test that the server response has the correct format and values."""
    upload_page = UploadPage(browser_context)
    try:
        upload_page.navigate("http://localhost:8000")
        response = upload_page.upload_file("valid_products.csv")

        # Parse response as JSON
        parsed_response = json.loads(response)

        # Validate response structure
        assert "status" in parsed_response
        assert "data" in parsed_response
        assert parsed_response["status"] == "success"

        # Validate data contents
        first_item = parsed_response["data"][0]
        expected_keys = {"id", "name", "price", "category", "stock"}
        assert expected_keys.issubset(first_item.keys())

        # Validate specific values
        assert first_item["id"] == 1
        assert first_item["name"] == "Laptop"
        assert first_item["price"] == 999.99
        assert first_item["category"] == "Electronics"
        assert first_item["stock"] == 50

    except Exception as e:
        browser_context.screenshot(path="error-screenshot.png")
        raise


def test_invalid_upload(browser_context):
    """Test uploading an invalid CSV file."""
    upload_page = UploadPage(browser_context)
    try:
        upload_page.navigate("http://localhost:8000")
        results = upload_page.upload_file("invalid_products.csv")
        assert "error" in results.lower()
    except Exception as e:
        browser_context.screenshot(path="error-invalid.png")
        raise


def test_nameless_upload(browser_context):
    """Test uploading a CSV file with missing names."""
    upload_page = UploadPage(browser_context)
    try:
        upload_page.navigate("http://localhost:8000")
        results = upload_page.upload_file("nameless_products.csv")
        assert "Missing name in row" in results
    except Exception as e:
        browser_context.screenshot(path="error-nameless.png")
        raise


def test_empty_file_upload(browser_context):
    """Test uploading an empty CSV file."""
    upload_page = UploadPage(browser_context)
    try:
        upload_page.navigate("http://localhost:8000")
        results = upload_page.upload_file("empty.csv")
        assert "No columns to parse from file" in results
    except Exception as e:
        browser_context.screenshot(path="error-empty.png")
        raise


def test_no_file_selected(browser_context):
    """Test clicking upload without selecting a file."""
    upload_page = UploadPage(browser_context)
    try:
        upload_page.navigate("http://localhost:8000")
        upload_page.click(upload_page.upload_button_selector)

        error_selector = "input:invalid"
        invalid_input = browser_context.query_selector(error_selector)
        assert invalid_input is not None, "No validation error triggered"
    except Exception as e:
        browser_context.screenshot(path="error-no-file.png")
        raise


if __name__ == "__main__":
    pytest.main(["-v", __file__])