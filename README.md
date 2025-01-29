# Shopic Automation Project

## Overview
This project automates the product upload system using Playwright with Python. It follows the Page Object Model (POM) structure for maintainability and readability.

## Project Structure
```
Shopic/
│── .venv/              # Virtual environment
│── assets/             # Additional assets (if needed)
│── pages/              # Page Object Model (POM) classes
│   │── __init__.py
│   │── base_page.py    # Base page class with common methods
│   │── upload_page.py  # Page object for the upload functionality
│── reports/            # Directory for test reports
│── tests/              # Test cases
│   │── __init__.py
│   │── test_upload.py  # Test script for file upload
│── ReadMe.docx         # Documentation
```

## Requirements
- Python 3.8+
- Playwright
- Pytest
- Other dependencies (see `requirements.txt` if available)

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Shopic
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install Playwright browsers:
   ```bash
   playwright install
   ```

## Running Tests
To execute the tests, run:
```bash
pytest tests/test_upload.py --html=reports/test_report.html
```
This will generate a test report in the `reports/` folder.

## Page Object Model (POM)
- `base_page.py`: Contains reusable methods like navigation, waiting for elements, etc.
- `upload_page.py`: Handles interactions with the upload page, such as filling forms and submitting files.

## Test Execution Reports
After running the tests, reports are stored in the `reports/` directory in HTML format.

## Assumptions and Limitations
- The application must be running locally at `http://localhost:8000`.
- The file upload feature accepts only CSV files.
- The project assumes a basic structure, and additional enhancements may be required.

=

