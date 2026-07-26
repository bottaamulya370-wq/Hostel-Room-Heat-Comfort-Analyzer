"""
suggestion_engine.py
---------------------
The "AI layer" of the project. This is a rule-based expert system:
a simple, explainable stand-in for AI reasoning.
"""


def suggest_action(score, humidity, occupancy, comfort_label):
    """Return a plain-English ventilation suggestion based on the readings."""

    if comfort_label == "Too Hot" and humidity > 65:
        return "Room is hot and humid: open windows and switch on exhaust fan."
    elif comfort_label == "Too Hot":
        return "Room is hot: increase ventilation, use ceiling fan on high."
    elif comfort_label == "Warm" and occupancy >= 3:
        return "Room is warm with several occupants: open a window for airflow."
    elif comfort_label == "Warm":
        return "Room is slightly warm: consider a fan or partial window opening."
    elif comfort_label == "Cold":
        return "Room is cold: close windows, reduce fan speed."
    else:
        return "Comfort level is acceptable: no action needed."