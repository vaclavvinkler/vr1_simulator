import streamlit as st
from models.reactor import Reactor
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def initialize_reactor():
    reactor = Reactor()

    # Konfigurace aktivní zóny (pouze jednou)
    for i in range(len(st.session_state.zone_config)):
        for j in range(len(st.session_state.zone_config)):
            if st.session_state.zone_config[i][j] in [None, "None"]:
                continue
            fuel_type = st.session_state.zone_config[i][j]
            reactor.add_fuel_rod(i, j, fuel_type)

    reactor.recalculate_main_stats()
    st.session_state.reactor = reactor
    st.session_state.reactor_output = {
        "power_map_data": reactor.get_power_map(),
        "outlet_temp": reactor.c_cycle.out_water_temp,
        "total_power": reactor.total_power
    }

def show_model_view():
    st.title("Reactor Simulation Results")

    rod_pos = st.slider("Control rod position (0 - 1)", 0.0, 1.0, 0.0, step=0.01)
    source_voltage = st.slider("Neutron source voltage (kV)", 0, 170, 120)
    flow_rate = st.number_input("Cooling flow rate (l/min)", value=3.0)
    inlet_temp = st.number_input("Inlet temperature (°C)", value=20.0, step=0.1)


    # Inicializuj reaktor jednou (pokud ještě není)
    if 'reactor' not in st.session_state:
        initialize_reactor()


    if st.button("Run simulation"):
        reactor = st.session_state.reactor
        # Nastav parametry dle UI

        reactor.control_rod.change_position_to(rod_pos)
        reactor.n_source.change_voltage_on_external_source(source_voltage)
        reactor.c_cycle.water_flow = flow_rate / (1000 * 60)
        reactor.c_cycle.in_water_temp = inlet_temp

        # Přepočítej hlavní statistiky
        reactor.recalculate_main_stats()

        # Aktualizuj výstupy
        st.session_state.reactor_output = {
            "power_map_data": reactor.get_power_map(),
            "outlet_temp": reactor.c_cycle.out_water_temp,
            "total_power": reactor.total_power
        }

    if "reactor_output" in st.session_state:
        power_map_data = st.session_state.reactor_output["power_map_data"]
        power_map = np.array(power_map_data).T

        outlet_temp = st.session_state.reactor_output["outlet_temp"]
        total_power = st.session_state.reactor_output["total_power"]

        st.markdown(f"**Total Power:** {(total_power):.2f} W")
        st.markdown(f"**Outlet Temperature:** {outlet_temp:.2f} °C")

        # Heatmapa výkonu
        st.markdown("### Max Power Distribution – Zone Cross-Section")

        fig, ax = plt.subplots(figsize=(6, 5))

        vmin = 0
        vmax = 50

        sns.heatmap(
            np.array(power_map),
            annot=True,
            fmt=".1f",
            cmap="plasma",
            ax=ax,
            vmin=vmin,
            vmax=vmax,
            square=True,
            cbar_kws={"label": "Power [W]"},
            linewidths = 2,
            linecolor = 'white'
        )

        # Přenastavení os na indexování od 1 místo 0
        ax.set_xticklabels([str(i + 1) for i in range(len(power_map[0]))])
        ax.set_yticklabels([str(i + 1) for i in range(len(power_map))], rotation=0)
        st.pyplot(fig)

        # Profil tyče
        st.markdown("### Inspect Fuel Rod Profile")
        i = st.number_input("Row (1–4)", min_value=1, max_value=4, value=1) -1
        j = st.number_input("Column (1–4)", min_value=1, max_value=4, value=1) -1

        if st.button("Show rod profile"):
            rod = st.session_state.reactor.core[i][j]
            if rod:
                profile = rod.get_axial_profile()

                heat_data = np.array(profile["power"]).reshape(-1, 1)

                vmin = 0
                vmax = 50

                fig2, ax2 = plt.subplots(figsize=(2, 6))
                sns.heatmap(
                    heat_data,
                    cmap="plasma",
                    cbar=True,
                    yticklabels= False,
                    xticklabels=False,
                    vmin=vmin,
                    vmax=vmax,
                    cbar_kws={"label": "Power [W]"},
                    ax=ax2
                )

                ax2.set_ylabel("Rod Height (m)")
                ax2.set_title(f"Power Profile for Rod ({i+1},{j+1})")

                st.pyplot(fig2)
