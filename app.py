"""
app.py
------
Hostel Room Heat Comfort Analyzer - Streamlit Web App

Combines:
  Physics        -> heat transfer formula
  Linear Algebra -> matrix-vector multiplication for comfort scoring
  Programming    -> Python + NumPy + CSV
  AI layer       -> rule-based ventilation suggestions
"""

import io
import csv
import numpy as np
import pandas as pd
import streamlit as st


# ----------------------------
# Physics + Linear Algebra
# ----------------------------

def heat_gain(T_in, T_out, h=1.0, A=1.0, occupancy=0, per_person_watts=0.0):
    """
    Heat transfer formula, with optional occupancy heat load:
        Q = h * A * (T_in - T_out) + (per_person_watts * occupancy)
    An average resting adult body gives off roughly 100W, so
    per_person_watts=100 (scaled down here to keep units consistent with
    the rest of the score) can be enabled from the sidebar.
    """
    return h * A * (T_in - T_out) + (per_person_watts * occupancy)


def build_reading_matrix(df, h=1.0, A=1.0, per_person_watts=0.0):
    """Build a NumPy matrix: columns = [T_in, humidity, occupancy, heat_gain]"""
    q = heat_gain(
        df["T_in"].astype(float), df["T_out"].astype(float),
        h=h, A=A,
        occupancy=df["occupancy"].astype(float),
        per_person_watts=per_person_watts
    )
    matrix = np.column_stack([
        df["T_in"].astype(float),
        df["humidity"].astype(float),
        df["occupancy"].astype(float),
        q
    ])
    return matrix


def comfort_scores(matrix, weights):
    """Comfort score = matrix . weights (matrix-vector product)"""
    return matrix @ np.array(weights)


def dominant_factor(matrix, factor_names):
    """
    Eigen-analysis (Linear Algebra bonus): find which factor contributes
    most to overall variation in the data, using the correlation matrix's
    eigenvector with the largest eigenvalue (i.e. the first principal
    component direction).
    """
    corr = np.corrcoef(matrix, rowvar=False)
    eigenvalues, eigenvectors = np.linalg.eig(corr)
    top_idx = np.argmax(eigenvalues)
    top_vector = np.abs(eigenvectors[:, top_idx])
    dominant_idx = np.argmax(top_vector)
    return factor_names[dominant_idx], eigenvalues, eigenvectors, top_idx


def predict_next_temperature(time_index, temperatures):
    """
    Simple linear regression (least-squares fit) using NumPy's polyfit:
        T_predicted = m * t + c
    Fits a straight line through past readings for one room and
    extrapolates one step ahead. This is a lightweight, explainable
    stand-in for a "predictive AI" feature.
    """
    if len(time_index) < 2:
        return None
    m, c = np.polyfit(time_index, temperatures, 1)  # degree-1 fit -> line
    next_t = time_index[-1] + 1
    predicted = m * next_t + c
    return predicted, m, c


def classify_comfort(score):
    if score < 45:
        return "Cold"
    elif score < 60:
        return "Comfortable"
    elif score < 75:
        return "Warm"
    else:
        return "Too Hot"


# ----------------------------
# AI layer (rule-based)
# ----------------------------

def suggest_action(humidity, occupancy, comfort_label):
    if comfort_label == "Too Hot" and humidity > 65:
        return "Open windows and switch on exhaust fan."
    elif comfort_label == "Too Hot":
        return "Increase ventilation, use ceiling fan on high."
    elif comfort_label == "Warm" and occupancy >= 3:
        return "Open a window for airflow."
    elif comfort_label == "Warm":
        return "Consider a fan or partial window opening."
    elif comfort_label == "Cold":
        return "Close windows, reduce fan speed."
    else:
        return "No action needed."


# ----------------------------
# Sample data (used if no CSV uploaded)
# ----------------------------

SAMPLE_CSV = """timestamp,room_id,T_in,T_out,humidity,occupancy
06:00,R101,26,22,60,2
06:00,R102,24,22,55,1
09:00,R101,29,27,65,3
09:00,R102,27,27,58,2
12:00,R101,33,34,70,4
12:00,R102,31,34,62,3
15:00,R101,35,36,75,4
15:00,R102,33,36,68,3
18:00,R101,30,29,72,4
18:00,R102,28,29,60,2
21:00,R101,27,24,66,3
21:00,R102,25,24,55,2
23:00,R101,23,20,58,1
23:00,R102,22,20,50,1
"""


# ----------------------------
# Streamlit UI
# ----------------------------

st.set_page_config(page_title="Hostel Room Heat Comfort Analyzer", layout="wide")

# --- Header row: title on the left, logo pinned top-right ---
header_left, header_right = st.columns([5, 1])
with header_left:
    st.title("🏠 Hostel Room Heat Comfort Analyzer")
    st.caption("Physics (heat transfer) + Linear Algebra (matrix scoring) + Rule-based AI suggestions")
with header_right:
    try:
        st.image("kietgroup.png", width=110)
    except Exception:
        st.caption("(logo not found — check filename/path)")

with st.expander("📐 Formulas Used"):
    st.markdown("**Heat transfer (Physics):**")
    st.latex(r"Q = h \cdot A \cdot (T_{in} - T_{out})")
    st.markdown("**Comfort score (Linear Algebra — matrix-vector product):**")
    st.latex(r"\vec{s} = X \cdot \vec{w}, \quad X = [T_{in},\ H,\ Occ,\ Q]")
    st.markdown("**Comfort classification (piecewise function):**")
    st.latex(r"""
    \text{Comfort}(s) =
    \begin{cases}
    \text{Cold} & s < 45 \\
    \text{Comfortable} & 45 \le s < 60 \\
    \text{Warm} & 60 \le s < 75 \\
    \text{Too Hot} & s \ge 75
    \end{cases}
    """)

# --- Sidebar: data input + weights ---
st.sidebar.header("1. Data")
uploaded_file = st.sidebar.file_uploader("Upload room_readings.csv", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Using your uploaded data.")
else:
    df = pd.read_csv(io.StringIO(SAMPLE_CSV))
    st.sidebar.info("Using built-in sample data.")

st.sidebar.header("2. Physics Constants (Q = h · A · (T_in - T_out))")
h_coeff = st.sidebar.slider("Heat transfer coefficient (h)", 0.1, 5.0, 1.0, 0.1)
area = st.sidebar.slider("Surface area (A, m²)", 0.1, 10.0, 1.0, 0.1)
include_body_heat = st.sidebar.checkbox("Include occupant body heat in Q", value=False)
per_person_watts = st.sidebar.slider(
    "Heat per person (scaled units)", 0.0, 10.0, 2.0, 0.5,
    disabled=not include_body_heat
) if True else 0.0
if not include_body_heat:
    per_person_watts = 0.0

st.sidebar.header("3. Comfort Score Weights")
w_temp = st.sidebar.slider("Temperature weight", 0.0, 3.0, 1.5, 0.1)
w_humidity = st.sidebar.slider("Humidity weight", 0.0, 3.0, 0.4, 0.1)
w_occupancy = st.sidebar.slider("Occupancy weight", 0.0, 3.0, 0.6, 0.1)
w_heat = st.sidebar.slider("Heat gain weight", 0.0, 3.0, 0.3, 0.1)

weights = [w_temp, w_humidity, w_occupancy, w_heat]

# --- Compute results ---
matrix = build_reading_matrix(df, h=h_coeff, A=area, per_person_watts=per_person_watts)
scores = comfort_scores(matrix, weights)

df["comfort_score"] = np.round(scores, 1)
df["comfort_label"] = [classify_comfort(s) for s in scores]
df["suggestion"] = [
    suggest_action(h, o, label)
    for h, o, label in zip(df["humidity"], df["occupancy"], df["comfort_label"])
]

# --- Display raw + result table (color-coded by comfort label) ---
st.subheader("📋 Room Readings & Comfort Report")

COMFORT_COLORS = {
    "Cold": "background-color: #cfe8ff",
    "Comfortable": "background-color: #d4f7dc",
    "Warm": "background-color: #fff3cd",
    "Too Hot": "background-color: #ffd6d6",
}

def highlight_comfort(row):
    color = COMFORT_COLORS.get(row["comfort_label"], "")
    return [color] * len(row)

st.dataframe(df.style.apply(highlight_comfort, axis=1), use_container_width=True)

# --- Chart: comfort score over time, per room ---
st.subheader("📈 Comfort Score Over Time")
chart_df = df.pivot_table(index="timestamp", columns="room_id", values="comfort_score")
st.line_chart(chart_df)

# --- Summary metrics ---
st.subheader("📊 Summary")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Avg Comfort Score", f"{df['comfort_score'].mean():.1f}")
col2.metric("Too Hot Readings", int((df["comfort_label"] == "Too Hot").sum()))
col3.metric("Comfortable Readings", int((df["comfort_label"] == "Comfortable").sum()))
col4.metric("Cold Readings", int((df["comfort_label"] == "Cold").sum()))

# --- Room comparison summary ---
st.subheader("🏘️ Room Comparison (Current Snapshot)")
latest_per_room = df.sort_values("timestamp").groupby("room_id").last().reset_index()
comp_cols = st.columns(len(latest_per_room))
for col, (_, row) in zip(comp_cols, latest_per_room.iterrows()):
    with col:
        st.markdown(f"**{row['room_id']}**")
        st.metric("Comfort Score", f"{row['comfort_score']}", row["comfort_label"])
        st.caption(row["suggestion"])

best_room = latest_per_room.loc[latest_per_room["comfort_score"].idxmin(), "room_id"]
worst_room = latest_per_room.loc[latest_per_room["comfort_score"].idxmax(), "room_id"]
st.info(f"🏆 Most comfortable right now: **{best_room}**  |  🔥 Needs attention: **{worst_room}**")

# --- Best time to ventilate, per room ---
st.subheader("🌬️ Best Time to Ventilate")
best_times = df.loc[df.groupby("room_id")["comfort_score"].idxmin()]
for _, row in best_times.iterrows():
    st.write(
        f"**{row['room_id']}** → coolest reading at **{row['timestamp']}** "
        f"(score {row['comfort_score']}, {row['comfort_label']}). "
        f"Best window to open windows / ventilate."
    )

# --- Correlation matrix (bonus linear algebra feature) ---
factor_names = ["T_in", "humidity", "occupancy", "heat_gain"]
with st.expander("🔍 Correlation Matrix (T_in, humidity, occupancy, heat_gain)"):
    corr = np.corrcoef(matrix, rowvar=False)
    corr_df = pd.DataFrame(corr, columns=factor_names, index=factor_names)
    st.dataframe(corr_df.round(2))

# --- Dominant factor analysis (eigenvalues/eigenvectors) ---
with st.expander("🧮 Dominant Factor Analysis (Eigenvalues/Eigenvectors)"):
    st.markdown(
        "Finds which factor drives comfort the most, using the eigenvector "
        "with the largest eigenvalue of the correlation matrix (first principal component)."
    )
    top_factor, eigenvalues, eigenvectors, top_idx = dominant_factor(matrix, factor_names)
    st.write(f"**Dominant factor:** `{top_factor}`")
    eig_df = pd.DataFrame({
        "Eigenvalue": np.round(eigenvalues, 3)
    }, index=factor_names)
    st.dataframe(eig_df)
    st.caption(
        f"Top eigenvector (principal component {top_idx+1}): "
        + ", ".join(f"{n}={v:.2f}" for n, v in zip(factor_names, eigenvectors[:, top_idx]))
    )

# --- Temperature prediction (linear regression, Linear Algebra bonus) ---
st.subheader("🔮 Next-Reading Temperature Prediction (Linear Regression)")
st.caption("Fits a straight line (least-squares) through each room's past T_in readings to predict the next one.")

pred_cols = st.columns(df["room_id"].nunique())
for col, room in zip(pred_cols, sorted(df["room_id"].unique())):
    room_df = df[df["room_id"] == room].reset_index(drop=True)
    time_index = np.arange(len(room_df))
    temps = room_df["T_in"].astype(float).values
    result = predict_next_temperature(time_index, temps)
    with col:
        st.markdown(f"**{room}**")
        if result is not None:
            predicted, slope, intercept = result
            trend = "rising 📈" if slope > 0 else "falling 📉" if slope < 0 else "stable ➡️"
            st.metric("Predicted next T_in (°C)", f"{predicted:.1f}")
            st.caption(f"Trend: {trend} (slope = {slope:.2f} °C/reading)")
        else:
            st.write("Not enough data points to predict.")

# --- Download results ---
st.subheader("⬇️ Download Report")
csv_bytes = df.to_csv(index=False).encode("utf-8")
st.download_button("Download comfort_report.csv", csv_bytes, "comfort_report.csv", "text/csv")
