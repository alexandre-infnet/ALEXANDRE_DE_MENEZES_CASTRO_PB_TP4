import streamlit as st


st.set_page_config(layout="wide")

pages = st.navigation(
    {
        "Home": [st.Page("pages/home/Home.py", title="AutoMatch", icon=":material/home:")],
        "Catalog": [
            st.Page(
                "pages/catalog/CatalogAdd.py",
                title="Add",
                icon=":material/add:",
            ),
            st.Page(
                "pages/catalog/CatalogSearch.py",
                title="Search",
                icon=":material/search:",
            ),
            st.Page(
                "pages/catalog/CatalogEnhance.py",
                title="Enhance",
                icon=":material/arrow_upward:",
            ),
        ],
        "Match!": [
            st.Page("pages/match/Match.py", title="Match", icon=":material/join:"),
        ],
    }
)

pages.run()
