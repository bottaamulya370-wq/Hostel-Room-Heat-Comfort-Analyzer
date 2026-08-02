import streamlit as st
import math

st.title("🌡 Heat Physics")
st.subheader("Heat Transfer Calculator")

st.write(
    "Calculate the heat transfer rate using Fourier's Law of Heat Conduction."
)

st.divider()

# -----------------------------
# User Inputs
# -----------------------------
k = st.number_input(
    "Thermal Conductivity (W/m·K)",
    min_value=0.1,
    value=0.8
)

area = st.number_input(
    "Wall Area (m²)",
    min_value=1.0,
    value=12.0
)

inside_temp = st.number_input(
    "Inside Temperature (°C)",
    value=30.0
)

outside_temp = st.number_input(
    "Outside Temperature (°C)",
    value=24.0
)

thickness = st.number_input(
    "Wall Thickness (m)",
    min_value=0.01,
    value=0.20
)

st.divider()

# -----------------------------
# Calculation
# -----------------------------
delta_t = inside_temp - outside_temp

heat_transfer = (k * area * delta_t) / thickness

st.metric(
    "Heat Transfer Rate (Q)",
    f"{heat_transfer:.2f} Watts"
)

st.latex(r"Q=\frac{kA(T_i-T_o)}{L}")

st.write("Where:")

st.markdown("""
- **Q** = Heat Transfer (Watts)
- **k** = Thermal Conductivity
- **A** = Surface Area
- **Ti** = Indoor Temperature
- **To** = Outdoor Temperature
- **L** = Wall Thickness
""")

st.divider()

# -----------------------------
# AI Suggestion
# -----------------------------
if heat_transfer > 300:
    st.error("🔥 High heat transfer detected. Improve wall insulation.")
elif heat_transfer > 150:
    st.warning("🌤 Moderate heat transfer. Ventilation is recommended.")
else:
    st.success("✅ Low heat transfer. Room insulation is good.")