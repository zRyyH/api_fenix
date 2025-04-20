from services.processar_leituras.data_fetcher import DataFetcher
from decorators.calc_error import error_handler
from logger import info, error
import json


class ProcessarLeituras:
    def __init__(self, condominio, data_da_leitura):
        self.data_da_leitura = data_da_leitura
        self.condominio = condominio

        self.fatcher = DataFetcher()
        self.raw = self.fatcher.obter_todos_dados(self.condominio, self.data_da_leitura)
        self.raw.update({"condominio": condominio})

        self.consumos_condominio = []
        self.consumos_unidades = []

        self.volume_consumido_concessionaria = None
        self.valor_concessionaria = 0

        self.volume_consumido_condominio = None
        self.total_arrecadado = 0
        self.residuo = None
        self.residuo_individual = None
        self.residuo_porcentual = None

    @error_handler
    def _calc_valor_individual(self, leitura):
        consumo = float(leitura["leitura"])
        total = 0.0

        for faixa in self.raw["faixas_de_consumo"]:
            faixa = faixa["faixas_de_consumo_id"]
            volume = max(
                0,
                min(consumo, float(faixa["consumo_maximo"]))
                - float(faixa["consumo_minimo"]),
            )

            total += volume * float(faixa["taxa"])

        if self.raw["tarifa"]["tarifa_de_esgoto"]:
            total *= 2

        info(f"Valor Individual: {total:.2f}, Consumo: {consumo:.2f}")

        return total

    @error_handler
    def _calc_valor_medicao_individual(self):
        valor_medicao = float(self.raw["tarifa"]["valor_de_medicao"])
        leituras = float(len(self.raw["leituras_unidades"]))

        return valor_medicao / float(leituras)

    @error_handler
    def _calc_valor_total_individual(self, valor_individual, valor_medicao_individual):
        total_individual = valor_individual

        if self.raw["tarifa"]["conta_zero"]:
            total_individual += self.residuo_individual

        if self.raw["tarifa"]["incluir_valor_medicao"]:
            total_individual += valor_medicao_individual

        return total_individual

    @error_handler
    def calc_arrecadacao(self):
        for leitura in self.raw["leituras_unidades"]:
            if not leitura["leitura"]:
                continue

            self.total_arrecadado += self._calc_valor_individual(leitura)

        info(f"Total Arrecadado: R$ {self.total_arrecadado:.2f}")

    @error_handler
    def calc_valor_concessionaria(self):
        porcentual = float(self.raw["tarifa"]["garantidora_percentual"])
        valor_da_conta = float(self.raw["leitura_concessionaria"][0]["valor_da_conta"])
        self.valor_concessionaria = valor_da_conta * (1 + porcentual / 100)
        info(f"Valor da conta: R$ {self.valor_concessionaria:.2f}")
        return self.valor_concessionaria

    @error_handler
    def calc_residuo(self):
        if self.total_arrecadado == 0:
            error("Total arrecadado é zero, não é possível calcular o resíduo.")
            return None

        self.residuo = self.valor_concessionaria - self.total_arrecadado
        self.residuo_individual = self.residuo / len(self.raw["leituras_unidades"])
        self.residuo_porcentual = (self.residuo / self.total_arrecadado) * 100
        info(
            f"Residuo: R$ {self.residuo:.2f} - Residuo Individual: R$ {self.residuo_individual:.2f} - Residuo Percentual: {self.residuo_porcentual:.2f}%"
        )
        return self.residuo, self.residuo_individual, self.residuo_porcentual

    @error_handler
    def calc_consumos_unidades(self):
        for leitura in self.raw["leituras_unidades"]:
            if not leitura["leitura"]:
                continue

            valor_individual = self._calc_valor_individual(leitura)
            valor_medicao_individual = self._calc_valor_medicao_individual()
            valor_residuo_individual = self.residuo_individual
            valor_total_individual = self._calc_valor_total_individual(
                valor_individual, valor_medicao_individual
            )

            self.consumos_unidades.append(
                {
                    "unidade_id": leitura["medidor_unidade_id"]["unidade_id"]["id"],
                    "data_da_proxima_leitura": leitura["data_da_proxima_leitura"],
                    "mes_de_referencia": leitura["mes_de_referencia"],
                    "data_da_leitura": leitura["data_da_leitura"],
                    "condominio_id": self.raw["condominio"]["id"],
                    "valor_residual": valor_residuo_individual,
                    "valor_medicao": valor_medicao_individual,
                    "valor_total": valor_total_individual,
                    "valor_individual": valor_individual,
                    "leitura": leitura["leitura"],
                    "foto_id": leitura["foto_id"],
                }
            )

        for i in self.consumos_unidades:
            info(f"Consumos Unidades: {json.dumps(i, indent=4)}")

        return self.consumos_unidades

    @error_handler
    def get(self):
        return self.raw
