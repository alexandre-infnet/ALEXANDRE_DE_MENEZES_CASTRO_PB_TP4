from pydantic import BaseModel


class Carro(BaseModel):
    Marca_do_Carro: str
    Ano_do_Carro: int
    Cilindros_do_Carro: int
    Litragem_do_Motor: float
    Modelo_do_Carro: str
    Tipo_de_Gasolina: str
    Cidade_MPG: float
    Rodovia_MPG: float
    Combinado_MPG: float
    Autonomia_Total_MPG: float
    Galoes_por_Milhas: float