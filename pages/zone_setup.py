# components/zone_setup.py
import streamlit as st
import pandas as pd
from models.fuel_types import fuel_types_dict



FUEL_TYPES = list(fuel_types_dict.keys())
FUEL_TYPES.insert(0,"None")

def show_zone_setup():
    st.title("Configure Reactor Core")
    st.markdown("### Click on a fuel rod to assign fuel")

    selected_rod = st.session_state.get("selected_rod")

    if selected_rod is None:
        st.warning("Není vybrán žádný prut (rod).")
        return

    try:
        i, j = selected_rod
    except (TypeError, ValueError):
        st.error("Vybraný prut není ve správném formátu.")
        return


    if "zone_config" not in st.session_state:
        st.session_state.zone_config = [[None for _ in range(4)] for _ in range(4)]

    if "selected_rod" not in st.session_state:
        st.session_state.selected_rod = None

    # Zobrazí 4x4 mřížku tlačítek, každé představuje jednu tyč
    cols = st.columns(4)
    for i in range(4):
        with cols[i]:
            for j in range(4):
                label = f"Rod ({i+1},{j+1})"
                button_key = f"btn_{i+1}_{j+1}"
                if st.button(label, key=button_key):
                    st.session_state.selected_rod = (i, j)

    # Pokud je nějaká tyč vybrána, zobrazí se menu pro výběr paliva
    if "selected_rod" in st.session_state:
        i, j = st.session_state.selected_rod
        st.markdown(f"### Set Fuel for Rod ({i+1}, {j+1})")
        selected_fuel = st.selectbox("Fuel type:", FUEL_TYPES, key="fuel_select")
        if selected_fuel:
            # Uložení paliva do konfigurační matice
            st.session_state.zone_config[i][j] = selected_fuel

    # Vizualizace aktuální konfigurace zóny jako tabulka
    st.markdown("### Current Zone Configuration")
    config_table = pd.DataFrame(
        [["None" if cell is None else FUEL_TYPES[FUEL_TYPES.index(cell)]
          for cell in row] for row in st.session_state.zone_config],
        columns=[f"Col {i}" for i in range(4)]
    )
    config_table.index = range(1, len(config_table)+1)
    config_table.columns = range(1, len(config_table) + 1)


    config_table = config_table.T


    st.dataframe(config_table)


# Při potvrzení zóny vytvoř reaktorový model
    if st.button("Confirm and simulate model"):

        # Přepni do stavu aplikace pro výpočty
        st.session_state.app_state = "model"

