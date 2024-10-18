import pandas as pd
import os


def calculate_pi(input_file):
    # Read the detected events
    df = pd.read_csv(input_file)

    # Count the number of events inside the circle
    n_detected = df["detected"].sum()
    n_total = len(df)

    # Estimate pi
    pi_estimate = n_detected / n_total * 4
    print(f"Estimated Pi: {pi_estimate}")


if __name__ == "__main__":
    INPUT_FILE = "data/detected_events.csv"

    calculate_pi(INPUT_FILE)
