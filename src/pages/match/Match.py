import requests
import streamlit as st
import pandas as pd


API_URL = "http://127.0.0.1:8000/processar_texto"

data = pd.read_csv('src/data/enhanced.csv')

st.title("Match!")


marca = st.multiselect("Brand", options=data['Marca do Carro'].unique(), default=None)
ano = st.multiselect("Year", options=data['Ano do Carro'].unique(), default=None)
faixa_preco_min, faixa_preco_max = st.slider(
    "Price range (USD)",
    min_value=float(data['Faixa de Preço (USD)'].min()),
    max_value=float(data['Faixa de Preço (USD)'].max()),
    value=(float(data['Faixa de Preço (USD)'].min()), float(data['Faixa de Preço (USD)'].max()))
)
categoria = st.multiselect("Category", options=data['Categoria do Carro'].unique(), default=None)
tracao = st.multiselect("Traction type", options=data['Tipo de Tração'].unique(), default=None)
transmissao = st.multiselect("Transmission", options=data['Tipo de Transmissão'].unique(), default=None)
assentos = st.multiselect("Seats", options=data['Número de Assentos'].unique(), default=None)
combustivel = st.multiselect("Fuel type", options=data['Tipo de Gasolina'].unique(), default=None)

if st.button("Match!"):
    with st.spinner("Processing filters..."):
        filtered_data = data.copy()

        if marca:
            filtered_data = filtered_data[filtered_data['Marca do Carro'].isin(marca)]
        if ano:
            filtered_data = filtered_data[filtered_data['Ano do Carro'].isin(ano)]
        filtered_data = filtered_data[
            (filtered_data['Faixa de Preço (USD)'] >= faixa_preco_min) &
            (filtered_data['Faixa de Preço (USD)'] <= faixa_preco_max)
        ]
        if categoria:
            filtered_data = filtered_data[filtered_data['Categoria do Carro'].isin(categoria)]
        if tracao:
            filtered_data = filtered_data[filtered_data['Tipo de Tração'].isin(tracao)]
        if transmissao:
            filtered_data = filtered_data[filtered_data['Tipo de Transmissão'].isin(transmissao)]
        if assentos:
            filtered_data = filtered_data[filtered_data['Número de Assentos'].isin(assentos)]
        if combustivel:
            filtered_data = filtered_data[filtered_data['Tipo de Gasolina'].isin(combustivel)]

        resultados = filtered_data.head(3)

        if not resultados.empty:
            payload = [
                {
                    "brand": row["Marca do Carro"],
                    "model": row["Modelo do Carro"],
                    "year": row["Ano do Carro"],
                    "price": row["Faixa de Preço (USD)"],
                    "category": row["Categoria do Carro"],
                    "traction_type": row["Tipo de Tração"],
                    "transmission": row["Tipo de Transmissão"],
                    "seats": row["Número de Assentos"],
                    "fuel_type": row["Tipo de Gasolina"],
                    "city_mpg": row["Cidade (MPG)"],
                    "highway_mpg": row["Rodovia (MPG)"],
                    "combined_mpg": row["Combinado (MPG)"],
                    "vehicle_size": row["Tamanho do Veículo"],
                    "maintenance_ease": row["Facilidade de Manutenção"],
                }
                for _, row in resultados.iterrows()
            ]

            try:
                response = requests.post(API_URL, json=payload)
                response.raise_for_status()
                response_data = response.json()

                st.write(response_data.get("response"))

            except requests.exceptions.RequestException as e:
                st.error(f"Erro na requisição: {e}")
        else:
            st.write("Nenhum veículo encontrado com os filtros selecionados.")