import os

from playwright.sync_api import Page, Locator
import random

class PageWrapper:
    def __init__(self, page: Page):
        self.page = page

    def _print_error(self, context: str, e: Exception):
        import traceback

        msg = f"Error {context}: {e}"
        payload = f"\n{'=' * 80}\n{msg}\n{traceback.format_exc()}\n{'=' * 80}\n"

        print(payload)

    def content(self) -> str:
        try:
            return self.page.content()
        except Exception as e:
            self._print_error("getting content", e)
            raise

    def title(self) -> str:
        try:
            return self.page.title()
        except Exception as e:
            self._print_error("getting title", e)
            raise

    def goto(self, url: str, retries: int = 2):
        attempts = 0
        while True:
            try:
                self.page.goto(url, wait_until="domcontentloaded")
                return
            except Exception as e:
                if attempts >= retries:
                    self._print_error(f"going to {url}", e)
                    raise

                attempts += 1
                self._print_error(f"going to {url} (attempt {attempts}/{retries})", e)
                # small random backoff before retrying
                self.sleep_random(500, 1500)

    def locator(self, selector: str, has_text: str | None = None) -> Locator:
        try:
            return self.page.locator(selector, has_text=has_text)
        except Exception as e:
            self._print_error(f'locating "{selector}"', e)
            raise

    def click(self, selector: str, has_text: str | None = None) -> bool:
        try:
            elm = self.locator(selector, has_text=has_text).first

            if elm is None:
                return False

            elm.click(no_wait_after=True)
            return True
        except Exception as e:
            self._print_error(f'clicking element "{selector}"', e)
            return False

    def click_coordinates(self, x: float, y: float) -> bool:
        try:
            self.page.mouse.click(x, y)
            return True
        except Exception as e:
            self._print_error(f'clicking coordinates ({x}, {y})', e)
            return False

    def inner_text(self, selector: str, has_text: str | None = None) -> str | None:
        try:
            return self.locator(selector, has_text=has_text).first.text_content()
        except Exception as e:
            self._print_error(f'getting text "{selector}"', e)
            return None
    
    def inner_texts(self, selector: str, has_text: str | None = None) -> list[str] | None:
        try:
            return self.locator(selector, has_text=has_text).all_text_contents()
        except Exception as e:
            self._print_error(
                f'getting texts "{selector}"',
                Exception("locator/all_text_contents failed"),
            )
            return None

    def get_texts(self, selector: str, has_text: str | None = None) -> list[str] | None:
        return self.inner_texts(selector, has_text=has_text)

    def get_attribute(
        self, selector: str, attribute: str, has_text: str | None = None
    ) -> str | None:
        try:
            return self.locator(selector, has_text=has_text).first.get_attribute(
                attribute
            )
        except:
            self._print_error(
                f'getting attribute "{attribute}" from "{selector}"',
                Exception("get_attribute failed"),
            )
            return None

    def get_attributes(
        self, selector: str, attribute: str, has_text: str | None = None
    ) -> list[str] | None:
        try:
            elms = self.locator(selector, has_text=has_text)
            return [
                attr
                for attr in [
                    el.get_attribute(attribute) for el in elms.element_handles()
                ]
                if attr is not None
            ]
        except:
            self._print_error(
                f'getting attributes "{attribute}" from "{selector}"',
                Exception("get_attributes failed"),
            )
            return None

    def fill(self, selector: str, value: str, has_text: str | None = None) -> bool:
        try:
            elm = self.locator(selector, has_text=has_text).first

            if elm is None:
                return False

            elm.fill(value)
            return True
        except Exception as e:
            self._print_error(f'filling element "{selector}"', e)
            return False

    def login(
        self,
        username_selector: str,
        password_selector: str,
        submit_selector: str,
        username: str,
        password: str,
    ) -> bool:
        try:
            self.fill(username_selector, username)
            self.sleep_random(500, 1000)
            self.fill(password_selector, password)
            self.sleep_random(500, 1000)
            self.click(submit_selector)
            self.sleep_random(500, 1000)
            return True
        except Exception as e:
            self._print_error("logging in", e)
            return False

    def wait_for_selector(self, selector: str, timeout: int = 5000, visible=True) -> bool:
        try:
            state = "visible" if visible else "attached"
            elm = self.page.wait_for_selector(selector, timeout=timeout, state=state)
            return elm is not None
        except Exception as e:
            self._print_error(f'waiting for "{selector}"', e)
            raise

    def wait_for_idle(self, timeout: int = 5000):
        try:
            self.page.wait_for_load_state("networkidle", timeout=timeout)
        except Exception as e:
            self._print_error("waiting for network idle", e)
            raise

    def exists(self, selector: str, has_text: str | None = None) -> bool:
        try:
            elm = self.locator(selector, has_text=has_text).first
            return elm is not None
        except Exception as e:
            return False

    def is_visible(self, selector: str, has_text: str | None = None) -> bool:
        try:
            elm = self.locator(selector, has_text=has_text)

            if elm is None:
                return False
            if elm.count() == 1:
                return elm.is_visible()
            
            # if multiple elements match, consider visible if at least one is visible
            for i in range(elm.count()):
                if elm.nth(i).is_visible():
                    return True
                
            return False
        
        except Exception as e:
            return False

    def hide(self, locator: Locator):
        try:
            locator.evaluate("e => e.setAttribute('hidden', true)")
        except Exception as e:
            self._print_error("hiding element", e)
            raise

    def sleep(self, ms: int):
        try:
            self.page.wait_for_timeout(ms)
        except Exception as e:
            self._print_error(f"sleeping for {ms}ms", e)
            raise

    def sleep_random(self, min_ms: int = 100, max_ms: int = 500):
        ms = random.randint(min_ms, max_ms)
        self.sleep(ms)

    def evaluate_js(self, script: str):
        try:
            return self.page.evaluate(script)
        except Exception as e:
            self._print_error("evaluating js", e)
            raise

    def evaluate_js_with_args(self, script: str, *args):
        try:
            return self.page.evaluate(script, *args)
        except Exception as e:
            self._print_error("evaluating js with args", e)
            raise
    
    def save_cookies(self, path: str = "cookies.json") -> None:
        path=f"cookies/{path}"

        try:
            self.page.context.storage_state(path=path)
        except Exception as e:
            self._print_error("saving cookies", e)
            raise
    
    def load_cookies_if_exists(self, path: str = "cookies.json") -> bool:
        path=f"cookies/{path}"
        
        try:
            import json
            import time

            if not os.path.exists(path):
                print(f"No cookies file found at '{path}', skipping loading cookies")
                return False
            with open(path, "r") as f:
                data = json.load(f)

            if isinstance(data, dict):
                cookies = data.get("cookies", [])
            elif isinstance(data, list):
                cookies = data
            else:
                raise Exception("cookies.json has unexpected format")

            now = time.time()
            valid_cookies = []
            expired_count = 0

            for c in cookies:
                if not isinstance(c, dict):
                    # unexpected shape, include to be safe
                    valid_cookies.append(c)
                    continue

                expiry = c.get("expires", c.get("expiry", None))

                # session cookies (no expiry or non-positive) should be loaded
                if expiry is None:
                    valid_cookies.append(c)
                    continue

                try:
                    expiry_val = float(expiry)
                except Exception:
                    # if expiry can't be parsed, load to be safe
                    valid_cookies.append(c)
                    continue

                # treat non-positive expiry as session/valid
                if expiry_val <= 0:
                    valid_cookies.append(c)
                    continue

                if expiry_val < now:
                    expired_count += 1
                    continue

                valid_cookies.append(c)

            if not valid_cookies:
                print(f"No valid cookies to load from '{path}' (all expired or none present)")
                return False

            self.page.context.add_cookies(valid_cookies)
            print(f"Loaded {len(valid_cookies)} cookies from '{path}' (skipped {expired_count} expired)")
            return True
        except Exception as e:
            self._print_error("loading cookies", e)
            raise

    def close(self):
        try:
            self.page.close()
        except Exception as e:
            self._print_error("closing page", e)
            raise
