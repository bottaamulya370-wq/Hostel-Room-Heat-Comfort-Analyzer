"""
main.py
-------
Hostel Room Heat Comfort Analyzer - entry point.

Pipeline:
  1. Read raw sensor readings from CSV
  2. Build a NumPy matrix of readings (Linear Algebra)
  3. Apply heat-transfer physics + compute comfort scores
  4. Classify comfort level
  5. Generate a ventilation suggestion (AI / rule-based layer)
  6. Log everything to an output CSV + print a summary table
"""

import csv
from comfort_calculator import build_reading_matrix, comfort_scores, classify_comfort
from suggestion_engine import suggest_action

INPUT_FILE = "data/room_readings.csv"
OUTPUT_FILE = "data/comfort_report.csv"


def load_readings(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main():
    rows = load_readings(INPUT_FILE)
    matrix = build_reading_matrix(rows)          # Linear Algebra step
    scores = comfort_scores(matrix)               # matrix . weights

    print(f"{'Time':<6}{'Room':<7}{'T_in':<6}{'Humid':<7}{'Occ':<5}{'Score':<8}{'Comfort':<12}Suggestion - main.py:33")
    print("" * 100)

    output_rows = []
    for row, score in zip(rows, scores):
        comfort_label = classify_comfort(score)
        suggestion = suggest_action(
            score, float(row["humidity"]), float(row["occupancy"]), comfort_label
        )

        print(f"{row['timestamp']:<6}{row['room_id']:<7}{row['T_in']:<6}{row['humidity']:<7} - main.py:43"
              f"{row['occupancy']:<5}{score:<8.1f}{comfort_label:<12}{suggestion}")

        output_rows.append({
            **row,
            "comfort_score": round(float(score), 1),
            "comfort_label": comfort_label,
            "suggestion": suggestion
        })

    # Log results to a new CSV
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=output_rows[0].keys())
        writer.writeheader()
        writer.writerows(output_rows)

    print(f"\nSaved detailed report to {OUTPUT_FILE} - main.py:59")


if __name__ == "__main__":
    main()