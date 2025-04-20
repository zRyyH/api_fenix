import traceback
from functools import wraps
from fastapi import HTTPException
from logger import error


def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            # se já for HTTPException, deixa o FastAPI lidar
            raise
        except Exception:
            # log completo do stack trace
            error(f"Erro na rota {func.__name__}: {traceback.format_exc()}")
            # retornamos um erro genérico ao cliente
            raise HTTPException(status_code=500, detail="Erro interno do servidor")

    return wrapper