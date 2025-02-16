import pytest
from pathlib import Path
from playwright.sync_api import sync_playwright
from pages.upload_page import UploadPage

# נתיב לתיקיית הקבצים
PROJECT_DIR = Path(__file__).parent
CSV_FILE_PATH = PROJECT_DIR / "data"

@pytest.fixture(scope="function")
def browser_page():
    """Fixture לפתיחת דפדפן ויצירת עמוד"""
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        yield page  # החזרת העמוד לבדיקה
        browser.close()



