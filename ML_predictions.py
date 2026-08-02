import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression

st.title("📈 Machine Learning Predictions")

df = pd.read_csv("data/hostel_data.csv")

X = df[["Humidity", "Occupancy"]]
y = df["Temperature"]

model = LinearRegression()
model.fit(X, y)

humidity = st.slider("Humidity", 30, 90, 60)
occupancy = st.slider("Occupancy", 0, 6, 2)

# Correct prediction input
input_data = pd.DataFrame({
    "Humidity": [humidity],
    "Occupancy": [occupancy]
})

prediction = model.predict(input_data)

st.metric(
    "Predicted Temperature",
    f"{prediction[0]:.2f} °C"
)

comfort = max(
    0,
    min(
        100,
        100 - abs(prediction[0] - 26) * 4 - abs(humidity - 60) * 0.5
    )
)

st.metric(
    "Predicted Comfort Score",
    f"{comfort:.1f}"
)

st.success("Prediction completed successfully.")