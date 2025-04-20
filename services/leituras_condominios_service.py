from repository.leituras_condominios import LeiturasCondominiosRepository
from repository.condominios import CondominiosRepository
from utils.data_utils import extrair_data
from logger import info, error, warning


# Classe de serviço para manipular leituras condominios
leituras_condominios_repository = LeiturasCondominiosRepository()


# Classe de serviço para manipular condominios
condominios_repository = CondominiosRepository()


def validar_leitura(medidor, leituras, payload):
    if not leituras:
        return True

    # Verifica se a leitura já existe para o medidor e o mês de referência
    for leitura in leituras:
        if leitura["medidor_condominio_id"] != medidor:
            continue

        mes_proxima_leitura = (
            extrair_data(payload.data_da_proxima_leitura)["ano_mes"]
            == extrair_data(leitura["data_da_proxima_leitura"])["ano_mes"]
        )

        mes_leitura_atual = (
            extrair_data(payload.data_da_leitura)["ano_mes"]
            == extrair_data(leitura["data_da_leitura"])["ano_mes"]
        )

        mes_referencia = (
            extrair_data(payload.mes_de_referencia)["ano_mes"]
            == extrair_data(leitura["mes_de_referencia"])["ano_mes"]
        )

        if mes_proxima_leitura or mes_leitura_atual or mes_referencia:
            warning(
                f"Leitura já existe para o medidor {medidor} no mês de referência {leitura['mes_de_referencia']}."
            )

            return False

    return True


def criar_leituras_condominios(payload):
    try:
        # Obter todas as leituras
        leituras = leituras_condominios_repository.obter_todos()

        # Obter todas as condominios
        condominios = condominios_repository.obter_todos()

        for condominio in condominios:
            for medidor_id in condominio["medidores_condominios_id"]:
                if validar_leitura(medidor_id, leituras, payload):
                    # Criar leitura para cada medidor da condominio
                    leituras_condominios_repository.criar_leituras(
                        {
                            "medidor_condominio_id": medidor_id,
                            "mes_de_referencia": payload.mes_de_referencia,
                            "data_da_leitura": payload.data_da_leitura,
                            "data_da_proxima_leitura": payload.data_da_proxima_leitura,
                            "status": "pendente",
                        }
                    )

                    info(
                        f"Leitura criada com sucesso para o medidor {medidor_id} no condominio {condominio['id']}."
                    )

        return True

    except Exception as e:
        raise Exception(f"Erro ao criar leituras: {str(e)}")
