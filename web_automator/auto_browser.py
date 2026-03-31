from contextlib import contextmanager

from camoufox import Camoufox

from .auto_page import AutoPage


class AutoBrowser:
    def __init__(self):
        self._browser = None

    @contextmanager
    def start_browser(
        self,
        headless: bool = True,
        humanize: bool = False,
        enable_cache: bool = True,
        block_images: bool = False,
    ):
        """
        Context manager that launches Camoufox and yields this wrapper.

            with AutoBrowser().start_browser() as browser:
                page = browser.new_page()
                page.goto("https://example.com")

        """

        with Camoufox(
            headless=headless,
            humanize=humanize,
            enable_cache=enable_cache,
            block_images=block_images,
            geoip=False,
        ) as browser:
        # with sync_playwright() as p:
        #     browser = p.chromium.launch(headless=headless)
            
            self._browser = browser
            try:
                yield self
            finally:
                self._browser.close()
                self._browser = None

    def new_page(self) -> AutoPage:
        if not self._browser:
            raise RuntimeError(
                "Browser not started. Use start_browser() context manager."
            )

        page = self._browser.new_page()

        return AutoPage(page)
