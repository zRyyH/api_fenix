from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class CondominiosRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_todos(self):
        return self.directus_api.get_directus(endpoint="/items/condominios")["data"]