import pandas as pd

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from helpers import adicionar_carro_no_csv

from entities.Carro import Carro


app = FastAPI()


@app.post("/carros/adicionar")
async def adicionar_carro(carro: Carro):
    """
    Adiciona um novo carro ao cars_data.csv.

    Este endpoint recebe os dados de um carro e adiciona ao arquivo `cars_data.csv`.

    - **carro**: Um objeto com os dados do carro a ser adicionado. O modelo de dados inclui:
        - **Marca_do_Carro**: A marca do carro.
        - **Ano_do_Carro**: O ano de fabricação do carro.
        - **Cilindros_do_Carro**: O número de cilindros do carro.
        - **Litragem_do_Motor**: A litragem do motor do carro.
        - **Modelo_do_Carro**: O modelo do carro.
        - **Tipo_de_Gasolina**: Tipo de combustível (ex: Gasolina, Etanol, etc).
        - **Cidade_MPG**: Consumo de combustível na cidade (milhas por galão).
        - **Rodovia_MPG**: Consumo de combustível na rodovia (milhas por galão).
        - **Combinado_MPG**: Consumo combinado (cidade e rodovia).
        - **Autonomia_Total_MPG**: Autonomia total do carro com o combustível disponível.
        - **Galoes_por_Milhas**: Quantidade de galões consumidos por milha.

    - Retorna:
        - Uma mensagem confirmando que o carro foi adicionado com sucesso.

    **Exemplo de corpo da requisição:**
    ```json
    {
        "Marca_do_Carro": "Toyota",
        "Ano_do_Carro": 2020,
        "Cilindros_do_Carro": 4,
        "Litragem_do_Motor": 2.5,
        "Modelo_do_Carro": "Corolla",
        "Tipo_de_Gasolina": "Gasolina",
        "Cidade_MPG": 30.0,
        "Rodovia_MPG": 38.0,
        "Combinado_MPG": 34.0,
        "Autonomia_Total_MPG": 400.0,
        "Galoes_por_Milhas": 0.03
    }
    ```
    """
    adicionar_carro_no_csv(carro)

    return {"message": "Carro adicionado com sucesso!"}


@app.get("/")
def read_root():
    """
    Endpoint principal da API.

    Este endpoint retorna uma mensagem de boas-vindas para a API de análise de carros.

    - Retorna:
        - Uma mensagem informando que a API está funcionando corretamente.
    """
    return {"message": "Bem-vindo à API de Recomendação de veículos!"}


@app.get("/carros")
def listar_carros(
    marca: str = Query(None, description="Filtrar por marca"),
    ano: int = Query(None, description="Filtrar por ano"),
    categoria: str = Query(None, description="Filtrar por categoria"),
):
    """
    Lista os carros registrados, com a possibilidade de filtragem por marca, ano e categoria.

    Este endpoint permite que o usuário consulte os dados de carros com base em critérios específicos, como marca, ano e categoria.

    - **marca** (opcional): Filtra os carros pela marca. Exemplo: "Toyota".
    - **ano** (opcional): Filtra os carros pelo ano de fabricação. Exemplo: 2020.
    - **categoria** (opcional): Filtra os carros pela categoria (ex: "Sedan", "SUV"). Exemplo: "Sedan".

    - Retorna:
        - Uma lista de carros com os filtros aplicados (retorna até 20 resultados).

    **Exemplo de requisição:**
    GET /carros?marca=Toyota&ano=2020&categoria=Sedan

    **Exemplo de resposta:**
    [
        {
            "Marca do Carro": "Toyota",
            "Ano do Carro": 2020,
            "Modelo do Carro": "Corolla",
            "Categoria do Carro": "Sedan",
            "Cilindros do Carro": 4,
            "Litragem do Motor": 2.5,
            "Tipo de Gasolina": "Gasolina",
            "Cidade (MPG)": 30.0,
            "Rodovia (MPG)": 38.0,
            "Combinado (MPG)": 34.0,
            "Autonomia Total (MPG)": 400.0,
            "Galões por Milhas": 0.03
        }
    ]
    """

    df = pd.read_csv("../data/enhanced.csv")
    filtro = df.copy()

    if marca:
        filtro = filtro[
            filtro["Marca do Carro"].str.contains(marca, case=False, na=False)
        ]

    if ano:
        filtro = filtro[filtro["Ano do Carro"] == ano]

    if categoria:
        filtro = filtro[
            filtro["Categoria do Carro"].str.contains(categoria, case=False, na=False)
        ]

    return JSONResponse(content=filtro.head(20).to_dict(orient="records"))
