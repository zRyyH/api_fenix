from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class FaixasDeConsumoRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_por_tarifa_id(self, tarifas_id):
        return self.directus_api.get_directus(
            endpoint=f"/items/faixas_de_consumo",
            params={"filter[tarifas_id][_in]": tarifas_id},
        )["data"]
