from jsonschema import ValidationError
import pandas as pd

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse

from helpers import adicionar_carro_no_csv

from entities.Carro import Carro
from entities.VehicleData import VehicleData

import google.generativeai as genai


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
    try:
        adicionar_carro_no_csv(carro)
        return {"message": "Carro adicionado com sucesso!"}

    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        raise HTTPException(status_code=500, detail="Erro interno no servidor")


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

@app.post("/processar_texto")
async def process_text(vehicles: list[VehicleData]):
    """
    Endpoint para processar os dados de veículos e gerar um texto detalhado usando o modelo Gemini.

    Args:
        vehicles (list[VehicleData]): Lista de veículos com detalhes para geração de texto.

    Returns:
        dict: Um dicionário contendo o prompt gerado e o texto retornado pelo modelo Gemini.

    Request Body:
        - `vehicles`: Uma lista de objetos com as seguintes propriedades:
            - `brand` (str): Marca do veículo.
            - `model` (str): Modelo do veículo.
            - `year` (int): Ano do modelo.
            - `price` (float): Preço do veículo em USD.
            - `category` (str): Categoria do veículo (ex.: Sedan, SUV).
            - `traction_type` (str): Tipo de tração (ex.: FWD, AWD).
            - `transmission` (str): Tipo de transmissão (ex.: Manual, Automático).
            - `seats` (int): Número de assentos.
            - `fuel_type` (str): Tipo de combustível (ex.: Gasolina, Diesel).
            - `city_mpg` (float): Consumo de combustível na cidade (miles per gallon - MPG).
            - `highway_mpg` (float): Consumo de combustível na rodovia (MPG).
            - `combined_mpg` (float): Consumo de combustível combinado (MPG).
            - `vehicle_size` (str): Tamanho do veículo (ex.: Compacto, Médio).
            - `maintenance_ease` (str): Facilidade de manutenção (ex.: Fácil, Moderado).

    Example:
        Request:
        ```json
        [
            {
                "brand": "Toyota",
                "model": "Corolla",
                "year": 2024,
                "price": 25000,
                "category": "Sedan",
                "traction_type": "FWD",
                "transmission": "Automatic",
                "seats": 5,
                "fuel_type": "Gasoline",
                "city_mpg": 30.5,
                "highway_mpg": 38.7,
                "combined_mpg": 34.6,
                "vehicle_size": "Medium",
                "maintenance_ease": "Moderate"
            }
        ]
        ```

        Response:
        ```json
        {
            "prompt": "You are a professional automotive reviewer. Write a detailed...",
            "response": "The Toyota Corolla 2024 is a well-rounded sedan ... [full analysis]"
        }
        ```

    Raises:
        HTTPException: Se ocorrer um erro durante a geração de texto ou processamento da requisição.
    """
    genai.configure(api_key="AIzaSyCOts1mwmF2GIF_FUiUYuujoDJe4DoTBsU")
    model = genai.GenerativeModel("gemini-1.5-flash")

    try:
        prompt = """
            You are a professional automotive reviewer. Write a detailed, insightful, and expert-level review for the following vehicles. Use a structured format, and highlight key features, advantages, and potential drawbacks. Add a summary recommendation for each vehicle.

            Include the following details:
            1. Overview of the vehicle's brand and model.
            2. Description of its target audience and market position.
            3. Performance analysis (e.g., engine specs, fuel efficiency, driving experience).
            4. Design features (e.g., interior and exterior highlights, comfort, material quality).
            5. Technology and innovation (e.g., advanced features, entertainment, safety systems).
            6. Final verdict with pros, cons, and a recommendation.

            Here are the vehicles to review:
        """

        for index, vehicle in enumerate(vehicles, start=1):
            vehicle_description = (
                f"\nVehicle {index}:\n"
                f"- Brand: {vehicle.brand}\n"
                f"- Model: {vehicle.model}\n"
                f"- Year: {vehicle.year}\n"
                f"- Price: ${vehicle.price} USD\n"
                f"- Category: {vehicle.category}\n"
                f"- Traction Type: {vehicle.traction_type}\n"
                f"- Transmission: {vehicle.transmission}\n"
                f"- Seats: {vehicle.seats}\n"
                f"- Fuel Type: {vehicle.fuel_type}\n"
                f"- City MPG: {vehicle.city_mpg}\n"
                f"- Highway MPG: {vehicle.highway_mpg}\n"
                f"- Combined MPG: {vehicle.combined_mpg}\n"
                f"- Vehicle Size: {vehicle.vehicle_size}\n"
                f"- Maintenance Ease: {vehicle.maintenance_ease}\n"
            )
            prompt += vehicle_description

        response = model.generate_content(prompt)

        return {"prompt": prompt, "response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))