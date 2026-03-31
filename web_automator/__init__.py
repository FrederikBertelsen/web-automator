"""web_automator package
This package provides a small wrapper around Playwright/Camoufox for simple web automation tasks.
"""

__version__ = "0.2.0"

from .browser_wrapper import BrowserWrapper
from .page_wrapper import PageWrapper

__all__ = ["BrowserWrapper", "PageWrapper", "__version__"]
