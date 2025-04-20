from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class TarifasRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_por_id(self, id):
        return self.directus_api.get_directus(endpoint=f"/items/tarifas/{id}")["data"]
