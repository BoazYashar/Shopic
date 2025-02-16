import pytest
from playwright.sync_api import Page, sync_playwright
from pathlib import Path
import json
from typing import Generator


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        self.page.goto(url, timeout=60000)

    def get_text(self, selector: str) -> str:
        return self.page.text_content(selector)

    def click(self, selector: str):
        self.page.click(selector)
