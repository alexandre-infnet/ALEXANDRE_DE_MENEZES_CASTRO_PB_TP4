import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Consultar Dados da API Enhanced",
    page_icon="🚀",
)

API_URL = "http://127.0.0.1:8000/carros"

st.title("Consulta de Carros API Enhanced")

tipo_input = st.selectbox(
    "Selecione tipo da consulta: ", ["", "Marca", "Ano", "Categoria"]
)

df = pd.read_csv("src/data/enhanced.csv")

marca_input = None
ano_input = None
categoria_input = None

if tipo_input == "Marca":
    marca_input = st.selectbox(
        "Selecione a marca do veículo",
        df["Marca do Carro"].unique(),
        index=0,
    )

if tipo_input == "Ano":
    ano_input = st.selectbox(
        "Selecione o ano do veículo",
        df["Ano do Carro"].unique(),
        index=0,
    )

if tipo_input == "Categoria":
    categoria_input = st.selectbox(
        "Selecione a categoria do veículo",
        df["Categoria do Carro"].unique(),
        index=0,
    )

if st.button("Consultar Carros"):
    try:
        params = {}
        if marca_input:
            params["marca"] = marca_input
        if ano_input:
            params["ano"] = ano_input
        if categoria_input:
            params["categoria"] = categoria_input

        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        carros_data = response.json()

        df_carros = pd.DataFrame(carros_data)
        st.write("Resultado da consulta:")
        st.dataframe(df_carros)

    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao consultar o endpoint: {e}")
