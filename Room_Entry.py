import streamlit as st
import pandas as pd

st.title("🏠 Room Entry")
st.subheader("Add Hostel Room Data")

# Load existing data
try:
    df = pd.read_csv("data/hostel_data.csv")
except FileNotFoundError:
    df = pd.DataFrame(columns=[
        "Room",
        "Block",
        "Floor",
        "Temperature",
        "Humidity",
        "Occupancy"
    ])

# -----------------------------
# Input Form
# -----------------------------
with st.form("room_form"):

    room = st.text_input("Room Number", "R107")

    block = st.selectbox(
        "Block",
        ["A", "B", "C"]
    )

    floor = st.selectbox(
        "Floor",
        [1,2,3,4,5]
    )

    temperature = st.slider(
        "Temperature (°C)",
        15.0,
        45.0,
        27.0
    )

    humidity = st.slider(
        "Humidity (%)",
        20,
        100,
        60
    )

    occupancy = st.slider(
        "Occupancy",
        0,
        6,
        2
    )

    submit = st.form_submit_button("➕ Add Room")

# -----------------------------
# Save Data
# -----------------------------
if submit:

    new_data = pd.DataFrame([{
        "Room": room,
        "Block": block,
        "Floor": floor,
        "Temperature": temperature,
        "Humidity": humidity,
        "Occupancy": occupancy
    }])

    df = pd.concat([df, new_data], ignore_index=True)

    df.to_csv("data/hostel_data.csv", index=False)

    comfort = (
        100
        - abs(temperature - 26) * 4
        - abs(humidity - 60) * 0.5
    )

    comfort = max(0, min(100, comfort))

    st.success("✅ Room Added Successfully")

    st.metric(
        "Comfort Score",
        f"{comfort:.1f}"
    )

# -----------------------------
# Display Data
# -----------------------------
st.divider()

st.subheader("📋 Current Room Data")

st.dataframe(df, width="stretch")