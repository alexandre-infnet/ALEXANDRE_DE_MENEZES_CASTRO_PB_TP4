from pydantic import BaseModel


class Carro(BaseModel):
    Marca_do_Carro: str
    Ano_do_Carro: int
    Cilindros_do_Carro: int
    Litragem_do_Motor: float
    Modelo_do_Carro: str
    Tipo_de_Gasolina: str
    Cidade_MPG: int
    Rodovia_MPG: int
    Combinado_MPG: int
    Autonomia_Total_MPG: int
    Galoes_por_Milhas: str
