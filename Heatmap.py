import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("🔥 Hostel Temperature Heatmap")
st.markdown("### Smart Room Heat Distribution")

# Load Data
df = pd.read_csv("data/hostel_data.csv")

# Make sure Room is text
df["Room"] = df["Room"].astype(str)

# ----------------------------
# Create Grid Automatically
# ----------------------------

n = len(df)
cols = 5  # Rooms per row

df["X"] = [(i % cols) + 1 for i in range(n)]
df["Y"] = [(i // cols) + 1 for i in range(n)]

# ----------------------------
# Heatmap
# ----------------------------

fig = px.scatter(
    df,
    x="X",
    y="Y",
    color="Temperature",
    size="Temperature",
    hover_name="Room",
    text="Room",
    color_continuous_scale="RdYlBu_r",
    title="Hostel Room Temperature Heatmap"
)

fig.update_traces(textposition="middle center")

fig.update_layout(
    xaxis_title="Room Position (X)",
    yaxis_title="Floor Position (Y)",
    height=650
)

st.plotly_chart(fig, width="stretch")

# ----------------------------
# Temperature Table
# ----------------------------

st.subheader("📋 Room Temperature Data")

st.dataframe(
    df[["Room", "Temperature", "Humidity", "Occupancy"]],
    width="stretch"
)

# ----------------------------
# Statistics
# ----------------------------

st.divider()

c1, c2, c3 = st.columns(3)

c1.metric("🔥 Maximum Temp", f"{df['Temperature'].max()} °C")
c2.metric("🌡 Average Temp", f"{df['Temperature'].mean():.1f} °C")
c3.metric("❄ Minimum Temp", f"{df['Temperature'].min()} °C")

st.success("✅ Heatmap Generated Successfully")