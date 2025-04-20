from functools import wraps
from logger import error
import traceback


def error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception:
            error(f"Erro na função {func.__name__}: {traceback.format_exc()}")
            raise Exception(f"Erro: {traceback.format_exc()}")

    return wrapper
