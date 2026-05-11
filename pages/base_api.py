from pages.locators import ScooterUrls


class BaseApi:
    """Базовый API-клиент: единый base URL и таймаут для всех вызовов"""

    def __init__(self, base_url=None, timeout=15):
        self.base_url = (base_url or ScooterUrls.BASE).rstrip("/")
        self.timeout = timeout

    def _url(self, path):
        if path.startswith("http"):
            return path
        return f"{self.base_url}{path}"
