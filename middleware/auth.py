from fastapi import Request, HTTPException
from constants.globals import DIRECTUS_CONFIG


async def verify_token(request: Request):
    try:
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Authentication required")

        if auth_header.split(" ")[1] == DIRECTUS_CONFIG["token"]:
            return True

    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")
