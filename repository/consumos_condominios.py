from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class ConsumosCondominiosRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_todos(self):
        return self.directus_api.get_directus(endpoint="/items/consumos_condominios")[
            "data"
        ]

    @error_handler
    def criar_consumos(self, payload):
        return self.directus_api.post_directus(
            endpoint="/items/consumos_condominios", json_data=payload
        )["data"]
