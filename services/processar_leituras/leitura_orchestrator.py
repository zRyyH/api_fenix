from services.processar_leituras.calcs.calculation import ProcessarLeituras
from repository.condominios import CondominiosRepository
from decorators.service_error import error_handler


class LeituraOrchestrator:
    def __init__(self):
        self.repo = CondominiosRepository()
        self.pipeline = []

    @error_handler
    def _set_pipeline(self, calcs):
        self.pipeline = [
            calcs.calc_valor_concessionaria,
            calcs.calc_arrecadacao,
            calcs.calc_residuo,
            calcs.calc_consumos_unidades,
        ]

    @error_handler
    def processar_leituras(self, data_da_leitura):
        for condominio in self.repo.obter_todos():
            self.calcs = ProcessarLeituras(condominio, data_da_leitura)
            self._set_pipeline(self.calcs)

            for step in self.pipeline:
                step()
