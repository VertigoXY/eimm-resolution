import random
import time
from gspread.exceptions import APIError
from requests.exceptions import RetryError


def request_with_backoff(func, max_retries=5):
    def wrapper(*args, **kwargs):
        i = 0
        while True:
            try:
                return func(*args, **kwargs)
            except APIError:
                if i == max_retries:
                    raise RetryError("Max retries exceeded")
                else:
                    wait = 2**i + random.uniform(0, 1)
                    time.sleep(wait)
                    i += 1
    return wrapper
