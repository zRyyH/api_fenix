from datetime import datetime


def extrair_data(data_str):
    """
    Função para extrair a data de uma string no formato ISO 8601.
    """
    try:
        try:
            data = datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S")
        except:
            data = datetime.strptime(data_str, "%Y-%m-%d")

        return {
            "ano_mes": data.strftime("%Y-%m"),
            "data": data,
            "ano": data.year,
            "mes": data.month,
            "dia": data.day,
        }

    except ValueError:
        raise ValueError("Formato de data inválido. Use o formato ISO 8601.")
