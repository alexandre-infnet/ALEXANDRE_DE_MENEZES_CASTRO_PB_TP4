import streamlit as st
import pandas as pd
from transformers import pipeline


# Carregar o modelo DistilGPT2 para geração de texto
@st.cache_resource
def load_model():
    return pipeline("text-generation", model="distilgpt2")


model_pipeline = load_model()


# Carregar o dataset
@st.cache_data
def load_data():
    return pd.read_csv("src/data/enhanced.csv")


data = load_data()

# Configuração da interface do Streamlit
st.title("Recomendador de Veículos")

st.write(
    """
    Este sistema recomenda veículos com base nas suas preferências. 
    Preencha o formulário abaixo e veja as opções personalizadas para você!
    """
)

# Formulário para entrada de dados
with st.form("vehicle_form"):
    faixa_preco = st.number_input(
        "Faixa de preço desejada (USD):", min_value=1000, max_value=200000, step=500
    )
    categoria = st.selectbox(
        "Categoria do Carro:", options=data["Categoria do Carro"].unique()
    )
    tipo_tracao = st.selectbox(
        "Tipo de Tração:", options=data["Tipo de Tração"].unique()
    )
    transmissao = st.selectbox(
        "Tipo de Transmissão:", options=data["Tipo de Transmissão"].unique()
    )
    num_assentos = st.slider("Número de Assentos:", min_value=2, max_value=7, value=5)
    preferencia_economia = st.radio("Prefere um veículo econômico?", ["Sim", "Não"])
    submit = st.form_submit_button("Enviar")

# Processar e gerar recomendações
if submit:
    st.subheader("Processando suas preferências...")
    user_preferences = {
        "Faixa de Preço": faixa_preco,
        "Categoria": categoria,
        "Tipo de Tração": tipo_tracao,
        "Transmissão": transmissao,
        "Número de Assentos": num_assentos,
        "Preferência por Economia": preferencia_economia,
    }

    # Filtrar veículos no dataset com base nas preferências
    filtered_data = data[
        (data["Faixa de Preço (USD)"] <= faixa_preco)
        & (data["Categoria do Carro"] == categoria)
        & (data["Tipo de Tração"] == tipo_tracao)
        & (data["Tipo de Transmissão"] == transmissao)
        & (data["Número de Assentos"] == num_assentos)
    ]

    if filtered_data.empty:
        st.error("Nenhum veículo encontrado com as preferências fornecidas.")
    else:
        # Selecionar até 3 veículos para detalhamento
        selected_vehicles = filtered_data.sample(n=min(3, len(filtered_data)))

        recommendations = []
        for _, vehicle in selected_vehicles.iterrows():
            # Gerar descrição detalhada para cada veículo
            input_text = (
                f"Detalhe este veículo: {vehicle['Marca do Carro']} {vehicle['Modelo do Carro']} "
                f"do ano {vehicle['Ano do Carro']}, categoria {vehicle['Categoria do Carro']}, "
                f"com tração {vehicle['Tipo de Tração']} e transmissão {vehicle['Tipo de Transmissão']}. "
                f"Econômico: {'Sim' if vehicle['Econômico'] else 'Não'}."
            )
            description = model_pipeline(
                input_text,
                max_length=100,
                num_return_sequences=1,
                do_sample=True,
                top_k=50,
                temperature=0.7,
            )[0]["generated_text"]
            recommendations.append(
                {
                    "Veículo": f"{vehicle['Marca do Carro']} {vehicle['Modelo do Carro']} ({vehicle['Ano do Carro']})",
                    "Descrição": description,
                }
            )

        # Exibir as recomendações
        st.subheader("Recomendações de Veículos:")
        for i, rec in enumerate(recommendations, start=1):
            st.write(f"**Opção {i}:** {rec['Veículo']}")
            st.write(rec["Descrição"])
