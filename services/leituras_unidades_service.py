from repository.leituras_unidades import LeiturasUnidadesRepository
from repository.unidades import UnidadesRepository
from utils.data_utils import extrair_data
from logger import info, error, warning


# Classe de serviço para manipular leituras unidades
leituras_unidades_repository = LeiturasUnidadesRepository()


# Classe de serviço para manipular unidades
unidades_repository = UnidadesRepository()


def validar_leitura(medidor, leituras, payload):
    if not leituras:
        return True

    # Verifica se a leitura já existe para o medidor e o mês de referência
    for leitura in leituras:
        if leitura["medidor_unidade_id"] != medidor:
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


def criar_leituras_unidades(payload):
    try:
        # Obter todas as leituras
        leituras = leituras_unidades_repository.obter_todos()

        # Obter todas as unidades
        unidades = unidades_repository.obter_todos()

        for unidade in unidades:
            for medidor_id in unidade["medidores_unidades_id"]:
                if validar_leitura(medidor_id, leituras, payload):
                    # Criar leitura para cada medidor da unidade
                    leituras_unidades_repository.criar_leituras(
                        {
                            "medidor_unidade_id": medidor_id,
                            "mes_de_referencia": payload.mes_de_referencia,
                            "data_da_leitura": payload.data_da_leitura,
                            "data_da_proxima_leitura": payload.data_da_proxima_leitura,
                            "status": "pendente",
                        }
                    )

                    info(
                        f"Leitura criada com sucesso para o medidor {medidor_id} na unidade {unidade['id']}."
                    )

        return True

    except Exception as e:
        raise Exception(f"Erro ao criar leituras: {str(e)}")
