"""web_automator package
This package provides a small wrapper around Playwright/Camoufox for simple web automation tasks.
"""

__version__ = "0.4.3"

from .browser_wrapper import BrowserWrapper
from .page_wrapper import PageWrapper
from .data_collector import DataCollector

__all__ = ["BrowserWrapper", "PageWrapper", "DataCollector", "__version__"]
