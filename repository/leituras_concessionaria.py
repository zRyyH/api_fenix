from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class LeiturasConcessionariaRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_todos(self):
        return self.directus_api.get_directus(
            endpoint="/items/leituras_concessionaria"
        )["data"]

    @error_handler
    def obter_por_condominio_id(self, condominio_id):
        return self.directus_api.get_directus(
            endpoint="/items/leituras_concessionaria",
            params={"filter[condominio_id][_eq]": condominio_id},
        )["data"]

    @error_handler
    def criar_leituras(self, payload):
        return self.directus_api.post_directus(
            endpoint="/items/leituras_concessionaria", json_data=payload
        )["data"]
