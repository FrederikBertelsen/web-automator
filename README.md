# web-automator

Small wrapper around Playwright/Camoufox to simplify browser automation.

Installation

- From GitHub (replace with your repo URL):

```
pip install git+https://github.com/FrederikBertelsen/web-automator.git
```

- Locally (from project root):

```
pip install .
# or (editable)
pip install -e .
```

Basic usage

```py
from web_automator import AutoBrowser

with AutoBrowser().start_browser() as browser:
    page = browser.new_page()
    page.goto("https://example.com")
```
