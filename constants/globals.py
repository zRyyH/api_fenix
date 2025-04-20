from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()


# Directus API configuration
DIRECTUS_CONFIG = {
    "url": os.getenv("DIRECTUS_URL_API"),
    "token": os.getenv("DIRECTUS_TOKEN"),
    "timeout": 60,
}


# API configuration
API_CONFIG = {
    "path_api": "/api/v1",
    "secret_key": os.getenv("DIRECTUS_TOKEN"),
    "port": int(os.getenv("API_PORT")),
    "host": os.getenv("API_HOST"),
    "reload": True,
}


# Project information
PROJECT_INFO = {
    "name": "API Customizada Para Hidrometrização",
    "description": "API para integração com o sistema de medição de água e gás",
    "version": "1.0.0",
    "author": "zRyyH",
}
