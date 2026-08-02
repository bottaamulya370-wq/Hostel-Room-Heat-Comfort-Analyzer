import streamlit as st
import pandas as pd

st.title("🤖 AI Thermal Advisor")

df = pd.read_csv("data/hostel_data.csv")

room = st.selectbox("Select Room", df["Room"])

room_data = df[df["Room"] == room].iloc[0]

temp = room_data["Temperature"]
humidity = room_data["Humidity"]
occupancy = room_data["Occupancy"]

st.metric("🌡 Temperature", f"{temp} °C")
st.metric("💧 Humidity", f"{humidity}%")
st.metric("👥 Occupancy", occupancy)

st.divider()

if temp >= 33:
    st.error("🔥 Room is extremely hot. Increase ventilation and use exhaust fans.")
elif temp >= 30:
    st.warning("🌤 Room is warm. Turn on ceiling fans and open windows.")
elif temp >= 26:
    st.success("✅ Room temperature is comfortable.")
else:
    st.info("❄ Room is cool and comfortable.")

st.subheader("💡 AI Suggestions")

tips = []

if temp > 30:
    tips.append("✔ Open windows for cross ventilation.")

if humidity > 65:
    tips.append("✔ Reduce humidity using exhaust fans.")

if occupancy > 3:
    tips.append("✔ High occupancy detected. Improve airflow.")

if not tips:
    tips.append("✔ Room conditions are optimal.")

for tip in tips:
    st.write(tip)