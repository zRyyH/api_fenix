from repository.faixas_de_consumo_tarifas import FaixasDeConsumoTarifasRepository
from repository.leituras_concessionaria import LeiturasConcessionariaRepository
from repository.leituras_condominios import LeiturasCondominiosRepository
from repository.consumos_condominios import ConsumosCondominiosRepository
from repository.leituras_unidades import LeiturasUnidadesRepository
from repository.consumos_unidades import ConsumosUnidadesRepository
from repository.tarifas import TarifasRepository


class DataFetcher:
    def __init__(self):
        self.consumos_condominios = ConsumosCondominiosRepository()
        self.concessionaria = LeiturasConcessionariaRepository()
        self.consumos_unidades = ConsumosUnidadesRepository()
        self.condominios = LeiturasCondominiosRepository()
        self.faixas = FaixasDeConsumoTarifasRepository()
        self.unidades = LeiturasUnidadesRepository()
        self.tarifas = TarifasRepository()

    def obter_todos_dados(self, condominio, data_da_leitura, data_da_leitura_anterior):
        leituras_unidades = self.unidades.obter_por_condominio_id(condominio["id"])
        tarifa = self.tarifas.obter_por_id(condominio["tarifa_id"][0])

        leitura_concessionaria = self.concessionaria.obter_por_condominio_id(
            condominio["id"]
        )

        leitura_condominio = self.condominios.obter_por_medidor_id(
            condominio["medidores_condominios_id"]
        )

        faixas_de_consumo = self.faixas.obter_por_tarifa_id(
            tarifa["faixas_de_consumo_id"]
        )

        consumos_unidades = self.consumos_unidades.obter_todos_por_condominio_id(
            condominio["unidades_id"]
        )

        consumos_condominio = self.consumos_condominios.obter_todos_por_condominio_id(
            condominio["id"]
        )

        return {
            "leitura_concessionaria": leitura_concessionaria,
            "leitura_condominio": leitura_condominio,
            "leituras_unidades": leituras_unidades,
            "faixas_de_consumo": faixas_de_consumo,
            "tarifa": tarifa,
        }
