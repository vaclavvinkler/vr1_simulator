import streamlit as st
from pages.zone_setup import show_zone_setup
from pages.model_view import show_model_view



st.set_page_config(
    page_title="VR-1 Nuclear Reactor Simulator",
    layout="centered",
    initial_sidebar_state="collapsed"
)
hide_sidebar_style = """
    <style>
        /* Skrýt sidebar a jeho toggle tlačítko */
        [data-testid="stSidebar"] {display: none;}
        [data-testid="collapsedControl"] {display: none;}
    </style>
"""

st.markdown(hide_sidebar_style, unsafe_allow_html=True)


# Inicializace session_state, pokud není nastavena
if "selected_rod" not in st.session_state or st.session_state.selected_rod is None:
    st.session_state.selected_rod = (0, 0)  # nebo jiná vhodná výchozí hodnota

def main():
    if "app_state" not in st.session_state:
        st.session_state.app_state = "setup"


    if st.session_state.app_state == "setup":
        show_zone_setup()

    elif st.session_state.app_state == "model":
        show_model_view()


if __name__ == "__main__":
    main()

