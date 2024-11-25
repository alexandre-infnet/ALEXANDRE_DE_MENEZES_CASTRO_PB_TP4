import requests

import streamlit as st


API_URL = "http://127.0.0.1:8000/carros/adicionar"

st.set_page_config(
    page_title="Adicionar veículos API Enhanced",
    page_icon="🚀",
)

st.title("Adicionar veículos")
st.text(
    "Adicione aqui os dados que não foram coletados ou encotrados no fueleconomy.gov"
)

marca = st.text_input("Marca do Carro")
ano = st.number_input("Ano do Carro", min_value=1900, max_value=2024, step=1)
cilindros = st.number_input("Cilindros do Carro", min_value=1, max_value=12, step=1)
litragem = st.number_input("Litragem do Motor", min_value=1.0, max_value=10.0, step=0.1)
modelo = st.text_input("Modelo do Carro")
tipo_gasolina = st.selectbox(
    "Tipo de Gasolina", ["Premium Gasoline", "Regular Gasoline"]
)
media_cidade = st.number_input("Cidade MPG", min_value=1, step=1)
media_rodovia = st.number_input("Rodovia MPG", min_value=1, step=1)
media_combinado = st.number_input("Combinado MPG", min_value=1, step=1)
autonomia = st.number_input("Autonomia Total MPG", min_value=1, step=1)
gal_por_mil = st.number_input("Galões por Milhas", min_value=0.1, step=0.1)

if st.button("Adicionar Carro"):
    data = {
        "Marca_do_Carro": f"{marca}",
        "Ano_do_Carro": f"{ano}",
        "Cilindros_do_Carro": f"{cilindros}",
        "Litragem_do_Motor": f"{litragem}",
        "Modelo_do_Carro": f"{modelo}",
        "Tipo_de_Gasolina": f"{tipo_gasolina}",
        "Cidade_MPG": f"{media_cidade}",
        "Rodovia_MPG": f"{media_rodovia}",
        "Combinado_MPG": f"{media_combinado}",
        "Autonomia_Total_MPG": f"{autonomia}",
        "Galoes_por_Milhas": f"{gal_por_mil}",
    }

    response = requests.post(API_URL, json=data)

    if response.status_code != 200:
        st.error("Não foi possível incluir o novo veículo")
    st.success("Veículo adicionado")
