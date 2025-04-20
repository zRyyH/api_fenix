from decorators.directus_error import error_handler
from constants.globals import DIRECTUS_CONFIG
import httpx
import json


class DirectusAPI:
    def __init__(self):
        self.client = httpx.Client(
            base_url=DIRECTUS_CONFIG["url"],
            headers={"Authorization": f"Bearer {DIRECTUS_CONFIG['token']}"},
            timeout=DIRECTUS_CONFIG["timeout"],
        )

    @error_handler
    def patch_directus(self, endpoint, json_data=None, params=None):
        response = self.client.patch(
            endpoint,
            json=json_data,
            params=params,
        )

        if "errors" in response.json().keys():
            log = json.dumps(response.json(), indent=4)
            raise Exception(f"Erro: {log}")

        return response.json()

    @error_handler
    def post_directus(self, endpoint, json_data=None, files=None, params=None):
        response = self.client.post(
            endpoint,
            json=json_data,
            files=files,
            params=params,
        )

        if "errors" in response.json().keys():
            log = json.dumps(response.json(), indent=4)
            raise Exception(f"Erro: {log}")

        return response.json()

    @error_handler
    def get_directus(self, endpoint, params=None):
        response = self.client.get(endpoint, params=params)

        if "errors" in response.json().keys():
            log = json.dumps(response.json(), indent=4)
            raise Exception(f"Erro: {log}")

        return response.json()
