import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Auto Refresh Every 3 Seconds
count = st_autorefresh(
    interval=3000,
    key="dashboard_refresh"
)
# Load Data
hostel = pd.read_csv("data/hostel_data.csv")
weather = pd.read_csv("data/weather_data.csv")
power = pd.read_csv("data/power_data.csv")

# Convert Room column to string
hostel["Room"] = hostel["Room"].astype(str)

# Simulate Live Sensor Data
hostel["Temperature"] += np.random.uniform(-0.8, 0.8, len(hostel))
hostel["Humidity"] += np.random.randint(-3, 4, len(hostel))
hostel["Occupancy"] = np.random.randint(1, 5, len(hostel))

weather.loc[0, "Temperature"] += np.random.uniform(-0.5, 0.5)
weather.loc[0, "Humidity"] += np.random.randint(-2, 3)

power.loc[0, "Daily_kWh"] += np.random.uniform(-0.5, 0.5)
# Comfort Score
hostel["Comfort Score"] = (
    100
    - abs(hostel["Temperature"] - 26) * 4
    - abs(hostel["Humidity"] - 60) * 0.5
)

hostel["Comfort Score"] = hostel["Comfort Score"].clip(0, 100)
st.title("🔥 ThermoHostel AI")

st.caption("Smart Hostel Room Heat Comfort Analyzer")

st.success(
    f"🟢 LIVE | Refresh Count : {count} | Updated : {datetime.now().strftime('%d-%m-%Y %I:%M:%S %p')}"
)

st.divider()
# ----------------------------------
# Top Cards
# ----------------------------------

col1, col2, col3 = st.columns(3)

# Weather Card
with col1:

    st.info("### 🌤 Live Weather")

    st.metric(
        "Outdoor Temperature",
        f"{weather.loc[0,'Temperature']:.1f} °C"
    )

    st.write(f"Humidity : {weather.loc[0,'Humidity']} %")
    st.write(f"Condition : {weather.loc[0,'Condition']}")

# Power Card
with col2:

    st.warning("### ⚡ Power Consumption")

    st.metric(
        "Daily Usage",
        f"{power.loc[0,'Daily_kWh']:.1f} kWh"
    )

    st.write(f"Monthly Cost : ₹{power.loc[0,'Monthly_Cost']}")
    st.write(f"Active Fans : {power.loc[0,'Active_Fans']}")

# Best Room Card
with col3:

    st.success("### 🏆 Best Room")

    best = hostel.loc[hostel["Comfort Score"].idxmax()]

    st.metric(
        label=f"Room {best['Room']}",
        value=f"{best['Comfort Score']:.1f}"
    )

    st.write(f"Temperature : {best['Temperature']:.1f} °C")
    st.write(f"Humidity : {best['Humidity']} %")

st.divider()
