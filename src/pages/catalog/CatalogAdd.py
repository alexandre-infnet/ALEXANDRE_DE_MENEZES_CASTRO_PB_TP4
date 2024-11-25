import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/carros/adicionar"

st.title(":material/space_dashboard: Catalog")
st.subheader(":material/add: Add")
st.divider()

with st.form(key="add_car_form", clear_on_submit=False):
    st.text("Infos")
    col1, col2, col3 = st.columns(3)
    with col1:
        marca = st.text_input("Marca do Carro")
    with col2:
        ano = st.number_input("Ano do Carro")
    with col3:
        cilindros = st.number_input("Cilindros do Carro")

    st.text("Details")
    col1, col2, col3 = st.columns(3)
    with col1:
        litragem = st.number_input("Litragem do Motor")
    with col2:
        modelo = st.text_input("Modelo do Carro")
    with col3:
        tipo_gasolina = st.selectbox("Tipo de Gasolina", ["Premium Gasoline", "Regular Gasoline"])

    st.text("Consume")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        media_cidade = st.number_input("Cidade MPG")
    with col2:
        media_rodovia = st.number_input("Rodovia MPG")
    with col3:
        media_combinado = st.number_input("Combinado MPG")
    with col4:
        autonomia = st.number_input("Autonomia Total MPG")
    with col5:
        gal_por_mil = st.number_input("Galões por Milhas")

    submit_button = st.form_submit_button(label="Add")

    if submit_button:
        errors = {}

        if not marca:
            errors["Marca_do_Carro"] = "Marca é obrigatória."
        if not modelo:
            errors["Modelo_do_Carro"] = "Modelo é obrigatório."
        if not (1900 <= ano <= 2024):
            errors["Ano_do_Carro"] = "Ano inválido."
        if not (1 <= cilindros <= 12):
            errors["Cilindros_do_Carro"] = "Cilindros inválidos."
        if not (1.0 <= litragem <= 10.0):
            errors["Litragem_do_Motor"] = "Litragem inválida."
        if not tipo_gasolina:
            errors["Tipo_de_Gasolina"] = "Tipo de gasolina é obrigatório."
        if not (media_cidade >= 1):
            errors["Cidade_MPG"] = "Cidade MPG inválido."
        if not (media_rodovia >= 1):
            errors["Rodovia_MPG"] = "Rodovia MPG inválido."
        if not (media_combinado >= 1):
            errors["Combinado_MPG"] = "Combinado MPG inválido."
        if not (autonomia >= 1):
            errors["Autonomia_Total_MPG"] = "Autonomia inválida."
        if not (gal_por_mil > 0):
            errors["Galoes_por_Milhas"] = "Galões por milhas inválido."

        if errors:
            for field, message in errors.items():
                st.error(f":material/cancel: {message}")
        else:
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
            else:
                st.success("Veículo adicionado com sucesso!")