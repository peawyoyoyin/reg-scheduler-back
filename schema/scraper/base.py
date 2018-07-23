def fallback_to(val):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except:
                return val
        return wrapper
    return decorator

def return_blank_on_fail(func):
    return fallback_to('')(func)

class BaseScraper:
    def __init__(self, soup):
        self._soup = soup
