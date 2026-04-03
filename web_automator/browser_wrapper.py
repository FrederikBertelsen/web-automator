from contextlib import contextmanager

from playwright.sync_api import sync_playwright

from .page_wrapper import PageWrapper


class BrowserWrapper:
    def __init__(self):
        self._browser = None
        self._context = None

    @contextmanager
    def start_browser(self, headless: bool = True, block_images: bool = False):
        with sync_playwright() as p:
            launch_args = [
                "--disable-dev-shm-usage",
                "--disable-features=Translate,BackForwardCache",
                "--disable-renderer-backgrounding",
                "--disable-background-timer-throttling",
                "--disable-backgrounding-occluded-windows",
            ]

            if headless:
                launch_args.append("--headless=new")

            browser = p.chromium.launch(
                headless=headless,
                args=launch_args,
            )

            self._browser = browser
            # create a browser context so we can set routing rules consistently
            self._context = self._browser.new_context()

            if block_images:
                def _block_images_route(route):
                    if route.request.resource_type == "image":
                        route.abort()
                    else:
                        route.continue_()

                self._context.route("**/*", _block_images_route)

            try:
                yield self
            finally:
                if self._context:
                    self._context.close()
                    self._context = None
                self._browser.close()
                self._browser = None

    def new_page(self) -> PageWrapper:
        if not self._browser:
            raise RuntimeError(
                "Browser not started. Use start_browser() context manager."
            )

        # Prefer creating pages from the context (so routing rules apply)
        if self._context:
            page = self._context.new_page()
        else:
            page = self._browser.new_page()

        return PageWrapper(page)
