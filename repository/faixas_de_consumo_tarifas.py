from integrations.directus_api import DirectusAPI
from decorators.repo_error import error_handler


class FaixasDeConsumoTarifasRepository:
    def __init__(self):
        self.directus_api = DirectusAPI()

    @error_handler
    def obter_por_tarifa_id(self, faixas_de_consumo_id):
        return self.directus_api.get_directus(
            endpoint=f"/items/faixas_de_consumo_tarifas",
            params={
                "filter[id][_in]": faixas_de_consumo_id,
                "fields": "*,faixas_de_consumo_id.*",
            },
        )["data"]
