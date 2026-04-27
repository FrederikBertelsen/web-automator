# web-automator

Small wrapper around Playwright to simplify browser automation.

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
from datetime import datetime
from web_automator import BrowserWrapper, DataCollector

def main():
    # Collect rows and print a few fields when each row is committed
    dc = DataCollector(print_on_flush=True, print_columns=["category", "title", "url"])

    # Start browser and collect a few rows
    with BrowserWrapper().start_browser(headless=True, block_images=True) as browser:
        page = browser.new_page()

        urls = [
            "https://example.com",
            "https://example.com/?ref=2",
        ]

        dc.set_field("category", "example pages")
        dc.set_current_row_as_base()

        for url in urls:
            page.goto(url)

            dc.set_field("title", page.title())
            dc.set_field("url", page.get_url())
            dc.commit_row()

    # Persist results to CSV
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_path = f"data/example_{timestamp}.csv"
    print(f"Saving data to '{csv_path}'")
    dc.save_csv(csv_path)

if __name__ == "__main__":
    main()
```

Login example

```py
import os
from web_automator import BrowserWrapper

def main():
    username = os.environ.get("EXAMPLE_USERNAME")
    password = os.environ.get("EXAMPLE_PASSWORD")
    if not username or not password:
        raise SystemExit("Set EXAMPLE_USERNAME and EXAMPLE_PASSWORD")

    with BrowserWrapper().start_browser(headless=True, block_images=True) as browser:
        page = browser.new_page()

        ok = page.login(
            login_url="https://example.com/login",

            username_selector="#username",
            password_selector="#password",
            submit_selector="button[type='submit']",

            username=username,
            password=password,

            # Either of these can be used as a success check:
            success_url_contains="/dashboard",
            success_selector="a[href='/logout']",

            # Optional: reuse cookies next run to avoid logging in again
            cookies_file="cookies/example_cookies.json",
        )

        if not ok:
            raise SystemExit("Login failed")

        page.goto("https://example.com/dashboard")
        print(page.title())

if __name__ == "__main__":
    main()
```
