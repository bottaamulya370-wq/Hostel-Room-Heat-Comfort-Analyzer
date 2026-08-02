import streamlit as st
import numpy as np
import pandas as pd

st.title("📐 Linear Algebra Module")
st.subheader("Matrix Operations for Hostel Data Analysis")

st.markdown("### Enter Matrix A")

col1, col2 = st.columns(2)

with col1:
    a11 = st.number_input("A11", value=1.0)
    a12 = st.number_input("A12", value=2.0)
    a21 = st.number_input("A21", value=3.0)
    a22 = st.number_input("A22", value=4.0)

matrix_a = np.array([
    [a11, a12],
    [a21, a22]
])

with col2:
    st.markdown("### Matrix A")
    st.dataframe(pd.DataFrame(matrix_a))

st.divider()

st.subheader("Matrix Properties")

st.write("### Transpose")
st.dataframe(pd.DataFrame(matrix_a.T))

st.write("### Determinant")
det = np.linalg.det(matrix_a)
st.success(f"{det:.2f}")

st.write("### Trace")
st.info(f"{np.trace(matrix_a):.2f}")

st.write("### Rank")
st.info(f"{np.linalg.matrix_rank(matrix_a)}")

st.divider()

st.subheader("Inverse Matrix")

if det != 0:
    inverse = np.linalg.inv(matrix_a)
    st.dataframe(pd.DataFrame(inverse))
else:
    st.error("Matrix is singular. Inverse does not exist.")

st.divider()

st.subheader("Eigen Values")

eigenvalues, eigenvectors = np.linalg.eig(matrix_a)

st.write("Eigen Values")
st.dataframe(pd.DataFrame(eigenvalues))

st.write("Eigen Vectors")
st.dataframe(pd.DataFrame(eigenvectors))

st.divider()

st.subheader("Application in ThermoHostel AI")

st.info("""
Linear Algebra is used in this project for:

• Matrix calculations

• Thermal data analysis

• Machine Learning algorithms

• Heatmap generation

• Data transformation

• Smart AI prediction models
""")