import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Sustainability Model", page_icon="🌍", layout="wide")

st.title("🌍 Manufacturing Carbon Footprint Model")
st.markdown("### Simulate the environmental impact of API Manufacturing parameters.")

# -----------------------------------------------------------------------------
# 1. SIDEBAR SIMULATION CONTROLS
# -----------------------------------------------------------------------------
st.sidebar.header("⚙️ Process Parameters")

# Energy Drivers
reaction_temp = st.sidebar.slider("Reaction Temperature (°C)", 20, 150, 80)
reaction_time = st.sidebar.slider("Reaction Time (Hours)", 1, 48, 12)
batch_size = st.sidebar.selectbox("Batch Size (kg)", [100, 500, 1000], index=1)

# Resource Drivers
solvent_volume = st.sidebar.number_input("Solvent Volume (L)", value=1200)
waste_recycling = st.sidebar.checkbox("Enable Solvent Recovery Unit", value=False)

# -----------------------------------------------------------------------------
# 2. CALCULATION ENGINE (Simple Physics)
# -----------------------------------------------------------------------------
def calculate_impact(temp, time, volume, recycling):
    # Constants (Fake emission factors based on Ecoinvent averages)
    # Grid Intensity: 0.4 kg CO2e / kWh
    
    # 1. Heating Energy: Q = m * c * deltaT (Simplified)
    heating_kwh = (volume * 4.18 * (temp - 20)) / 3600  # Specific heat of water approx
    
    # 2. Maintaining Temp (Heat loss over time)
    maintenance_kwh = (0.5 * time) * (temp / 100) 
    
    # 3. Pumping/Mixing Energy
    mechanical_kwh = 2.5 * time # 2.5 kW motor
    
    total_energy = heating_kwh + maintenance_kwh + mechanical_kwh
    
    # 4. Waste Impact (Incineration vs Recycling)
    if recycling:
        waste_kg_co2 = volume * 0.1 # Low impact (recovery energy)
    else:
        waste_kg_co2 = volume * 2.5 # High impact (incineration)
        
    energy_kg_co2 = total_energy * 0.4 # Grid factor
    
    return {
        "Heating (Scope 2)": heating_kwh * 0.4,
        "Mechanical (Scope 2)": (maintenance_kwh + mechanical_kwh) * 0.4,
        "Waste Disposal (Scope 3)": waste_kg_co2
    }

impacts = calculate_impact(reaction_temp, reaction_time, solvent_volume, waste_recycling)
total_co2 = sum(impacts.values())

# -----------------------------------------------------------------------------
# 3. DASHBOARD VISUALS
# -----------------------------------------------------------------------------
col1, col2, col3 = st.columns(3)
col1.metric("Total Batch Carbon", f"{total_co2:.1f} kg CO₂e", delta=f"{'-' if waste_recycling else '+'} Impact")
col2.metric("Energy Intensity", f"{(total_co2/batch_size):.2f} kg CO₂/kg API")
col3.metric("Solvent Recovery", "Active" if waste_recycling else "Disabled", delta_color="off")

st.divider()

c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Emission Hotspots")
    # Prepare data for Altair
    df_chart = pd.DataFrame(list(impacts.items()), columns=["Source", "Emissions (kg CO2e)"])
    
    chart = alt.Chart(df_chart).mark_bar().encode(
        x='Emissions (kg CO2e)',
        y=alt.Y('Source', sort='-x'),
        color=alt.Color('Source', legend=None)
    ).properties(height=300)
    
    st.altair_chart(chart, use_container_width=True)

with c2:
    st.info("""
    **Model Logic:**
    * **Heating:** calculated based on specific heat capacity relative to baseline (20°C).
    * **Scope 2:** Assumes US Grid avg (0.4 kg CO2/kWh).
    * **Scope 3:** Simulates trade-off between *Solvent Incineration* vs. *Distillation/Recovery*.
    """)
