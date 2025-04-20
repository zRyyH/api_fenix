from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class ConsumosUnidadesRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_todos_por_unidade_id(self, unidade_id):
        return self.directus_api.get_directus(
            endpoint="/items/consumos_unidades",
            params={
                "filter[unidade_id][_eq]": unidade_id,
            },
        )["data"]

    @error_handler
    def criar_consumos(self, payload):
        return self.directus_api.post_directus(
            endpoint="/items/consumos_unidades", json_data=payload
        )["data"]
