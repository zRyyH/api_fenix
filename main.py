from constants.globals import API_CONFIG, PROJECT_INFO
from fastapi import FastAPI
from routers import api
import uvicorn


app = FastAPI(
    title=PROJECT_INFO["name"],
    description=PROJECT_INFO["description"],
    version=PROJECT_INFO["version"],
)


app.include_router(api.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["reload"],
    )
