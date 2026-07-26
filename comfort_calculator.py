"""
comfort_calculator.py
----------------------
Physics + Linear Algebra layer of the Hostel Room Heat Comfort Analyzer.
"""

import numpy as np


def heat_gain(T_in, T_out, h=1.0, A=1.0):
    """
    Simplified heat transfer formula (Newton's Law of Cooling style):
        Q = h * A * (T_in - T_out)

    Q > 0 -> room losing heat to outside (outside is cooler)
    Q < 0 -> room gaining heat from outside (outside is hotter)
    """
    return h * A * (T_in - T_out)


def build_reading_matrix(rows):
    """
    Convert CSV rows into a NumPy matrix.
    Columns: [T_in, humidity, occupancy, heat_gain]
    Each row = one (room, time) reading.
    """
    matrix = []
    for r in rows:
        q = heat_gain(float(r["T_in"]), float(r["T_out"]))
        matrix.append([
            float(r["T_in"]),
            float(r["humidity"]),
            float(r["occupancy"]),
            q
        ])
    return np.array(matrix)


def comfort_scores(matrix, weights=None):
    """
    Linear Algebra step: comfort score = matrix . weights (matrix-vector product)

    Default weights:
        T_in       -> 1.5
        humidity   -> 0.4
        occupancy  -> 0.6
        heat_gain  -> 0.3
    """
    if weights is None:
        weights = np.array([1.5, 0.4, 0.6, 0.3])
    return matrix @ weights


def classify_comfort(score):
    """Turn a numeric score into a comfort category."""
    if score < 45:
        return "Cold"
    elif score < 60:
        return "Comfortable"
    elif score < 75:
        return "Warm"
    else:
        return "Too Hot"