import pandas as pd

import streamlit as st


st.title(":material/space_dashboard: Catalog")
st.subheader(":material/arrow_upward: Enhance")

st.download_button(
    label=":material/download: Download Diminished Data",
    data="src/data/cars_data.csv",
    file_name="cars_data.csv",
    mime="text/csv",
)

st.divider()


@st.cache_data
def load_car_data():
    cars_df = pd.read_csv("src/data/cars_data.csv")

    if "uploaded_df" in st.session_state:
        uploaded_df = st.session_state.uploaded_df

        enhanced_df = pd.merge(
            uploaded_df,
            cars_df,
            on=["Marca do Carro", "Ano do Carro", "Modelo do Carro"],
            how="inner",
        )

        enhanced_df.to_csv("src/data/enhanced.csv", index=False)

        return enhanced_df
    else:
        st.error("Please, upload a CSV File.")
        return None


st.subheader("Upload requirements")
st.markdown("If you want to upload the data, it must follow the schema below:")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    - **Marca do Carro**
    - **Ano do Carro**
    - **Modelo do Carro**
    - **Faixa de Preço (USD)**
    - **Categoria do Carro**
    - **Número de Airbags**
    - **Sistema de Assistência de Motorista**
    - **Classificação de Segurança (Estrelas)**
    - **Tempo de Garantia (Anos)**
    """)

with col2:
    st.markdown("""
    - **Facilidade de Manutenção**
    - **Estilo da Roda**
    - **Tamanho da Roda**
    - **Teto Solar**
    - **Número de Assentos**
    - **Material do Assento**
    - **Ar Condicionado**
    - **Entretenimento**
    - **Start/Stop**
    """)

with col3:
    st.markdown("""
    - **Partida sem Chave**
    - **Tipo de Tração**
    - **Tipo de Transmissão**
    - **Torque (Nm)**
    - **Potência do Motor (hp)**
    - **Suspensão**
    - **Freios**
    - **Tamanho do Porta Malas (L)**
    - **Quantidade de Portas**
    - **Tamanho do Veículo**
    """)

st.divider()

car_enchanter = st.file_uploader("Enhance data: ", type="csv")
if not car_enchanter:
    st.warning(":material/info: Use the file user_data.csv")

if car_enchanter:
    st.session_state.uploaded_df = pd.read_csv(car_enchanter)

    enhanced_df = load_car_data()

    if enhanced_df is not None:
        st.success("Successfully uploaded")
        st.dataframe(enhanced_df)
