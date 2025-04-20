from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class LeiturasCondominiosRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_todos(self):
        return self.directus_api.get_directus(endpoint="/items/leituras_condominios")[
            "data"
        ]

    @error_handler
    def obter_por_medidor_id(self, medidor_condominio_id):
        return self.directus_api.get_directus(
            endpoint="/items/leituras_condominios",
            params={"filter[medidor_condominio_id][_eq]": medidor_condominio_id},
        )["data"]

    @error_handler
    def criar_leituras(self, payload):
        return self.directus_api.post_directus(
            endpoint="/items/leituras_condominios", json_data=payload
        )["data"]
