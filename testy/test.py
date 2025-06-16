# components/model_view.py
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def show_model_view():
    st.title("Reactor Simulation Results")

    # UI ovladače: pozice regulačních tyčí, neutronový zdroj, průtok, teplota
    rod_pos = st.slider("Control rod position (0 - 1)", 0.0, 1.0, 0.0, step=0.01)
    source_voltage = st.slider("Neutron source voltage (kV)", 0, 170, 120)
    flow_rate = st.number_input("Cooling flow rate (l/min)", value=3.0)
    inlet_temp = st.number_input("Inlet temperature (°C)", value=20.0, step=0.1)

    from models.reactor import Reactor
    reactor = Reactor()

    # Konfigurace aktivní zóny
    for i in range(len(st.session_state.zone_config)):
        for j in range(len(st.session_state.zone_config)):
            if st.session_state.zone_config[i][j] == None or st.session_state.zone_config[i][
                j] == "None":  # pozn: bo jsem kokot uvažuji i None jako text
                continue

            # nakonfiguruje jednotlivé platné tyče do zóny
            fuel_type = st.session_state.zone_config[i][j]
            reactor.add_fuel_rod(i, j, fuel_type)

    reactor.recalculate_main_stats()

    st.session_state.reactor_output = {
        # "power_map": reactor.get_power_map(),
        "outlet_temp": reactor.c_cycle.out_water_temp,
        "total_power": reactor.total_power
    }

    if st.button("Run simulation"):
        # změní parametry ze vstupů aplikace
        reactor.control_rod.change_position_to(rod_pos)  # posune tyč
        reactor.n_source.change_voltage_on_external_source(source_voltage)  # změní příkon externího neutronového zdroje
        reactor.c_cycle.water_flow = flow_rate / (1000 * 60)  # změní průtok vody
        reactor.c_cycle.in_water_temp = inlet_temp  # změní teplotu přívodní vody do chladnícího cyklu

        # prepočítá hlavní údaje
        reactor.recalculate_main_stats()

        # Výstupy – ulož do session_state
        st.session_state.reactor_output = {
            # "power_map": reactor.get_power_map(),
            "outlet_temp": reactor.c_cycle.out_water_temp,
            "total_power": reactor.total_power
        }

        # Pokud už existuje výsledek, zobraz grafy
        if "reactor_output" in st.session_state:
            """power_map = st.session_state.reactor_output["power_map"]"""
            outlet_temp = st.session_state.reactor_output["outlet_temp"]
            total_power = st.session_state.reactor_output["total_power"]

            # Hlavní přehled
            st.markdown(f"**Total Power:** {(total_power / 1000):.2f} kW")
            st.markdown(f"**Outlet Temperature:** {outlet_temp:.2f} °C")

            """# Heatmapa výkonu
            st.markdown("### Power Map (Top View)")
            fig, ax = plt.subplots()
            sns.heatmap(np.array(power_map), annot=True, fmt=".1f", cmap="hot", ax=ax)
            st.pyplot(fig)

            # Detailní profil tyče
            st.markdown("### Inspect Fuel Rod Profile")
            i = st.number_input("Row (0–3)", min_value=0, max_value=3, value=0)
            j = st.number_input("Column (0–3)", min_value=0, max_value=3, value=0)

            if st.button("Show rod profile"):
                # 💡 Získání profilových dat z modelu
                rod = st.session_state.fuel_rod_matrix[i][j]
                if rod:
                    profile = rod.get_axial_profile()  # např. výkon vs výška

                    fig2, ax2 = plt.subplots()
                    ax2.plot(profile["z"], profile["power"])
                    ax2.set_xlabel("Rod Height (cm)")
                    ax2.set_ylabel("Power Density")
                    st.pyplot(fig2)"""
