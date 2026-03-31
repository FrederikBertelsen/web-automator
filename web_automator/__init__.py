"""web_automator package

This package provides a small wrapper around Playwright/Camoufox for
simple web automation tasks.
"""

__version__ = "0.1.0"

from .auto_browser import AutoBrowser
from .auto_page import AutoPage

__all__ = ["AutoBrowser", "AutoPage", "__version__"]
