import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


API_URL = "http://127.0.0.1:8000/carros"

st.title(":material/space_dashboard: Catalog")
st.subheader(":material/search: Search")
st.divider()

df = pd.read_csv("src/data/enhanced.csv")

marca_input = None
ano_input = None
categoria_input = None

marca_input = st.sidebar.selectbox(
    "Brand",
    [""] + sorted(df["Marca do Carro"].unique()),
)

ano_input = st.sidebar.selectbox(
    "Year",
    [""] + sorted(df["Ano do Carro"].unique().astype(str).tolist()),
)

categoria_input = st.sidebar.selectbox(
    "Category",
    [""] + sorted(df["Categoria do Carro"].unique()),
)

if st.sidebar.button(":material/search: Search"):
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
        if df_carros.empty:
            st.error(":material/cancel: Sorry! No cars found")
        else:
            st.text("Data")
            st.dataframe(df_carros)
            st.text("Statistics")
            st.write(df_carros.describe())

            st.text("Word Cloud")
            text = " ".join(df_carros["Modelo do Carro"])
            wordcloud = WordCloud(
                width=800, height=400, background_color="white"
            ).generate(text)

            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation="bilinear")
            plt.axis("off")
            st.pyplot(plt)

    except requests.exceptions.RequestException as e:
        st.error(f"Error requesting the endpoint: {e}")
