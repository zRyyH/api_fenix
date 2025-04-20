from pydantic import BaseModel


# Defina o modelo do JSON esperado
class ProcessarLeituras(BaseModel):
    data_da_leitura: str