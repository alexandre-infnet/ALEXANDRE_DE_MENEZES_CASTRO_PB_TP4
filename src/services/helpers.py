import pandas as pd

from entities.Carro import Carro


def adicionar_carro_no_csv(carro: Carro):
    df = pd.read_csv("../data/cars_data.csv")

    novo_carro = pd.DataFrame(
        [
            {
                "Marca do Carro": carro.Marca_do_Carro,
                "Ano do Carro": carro.Ano_do_Carro,
                "Cilindros do Carro": carro.Cilindros_do_Carro,
                "Litragem do Motor": carro.Litragem_do_Motor,
                "Modelo do Carro": carro.Modelo_do_Carro,
                "Tipo de Gasolina": carro.Tipo_de_Gasolina,
                "Cidade (MPG)": carro.Cidade_MPG,
                "Rodovia (MPG)": carro.Rodovia_MPG,
                "Combinado (MPG)": carro.Combinado_MPG,
                "Autonomia Total (MPG)": carro.Autonomia_Total_MPG,
                "Galões por Milhas": carro.Galoes_por_Milhas,
            }
        ]
    )

    novo_carro.index = [df.index.max() + 1]
    df = pd.concat([df, novo_carro])

    df.to_csv("../data/cars_data.csv", index=False)
