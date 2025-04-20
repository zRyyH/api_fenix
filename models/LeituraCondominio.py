from pydantic import BaseModel


# Defina o modelo do JSON esperado
class LeituraCondominio(BaseModel):
    mes_de_referencia: str
    data_da_leitura: str
    data_da_proxima_leitura: str
