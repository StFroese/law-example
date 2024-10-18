import pandas as pd
import numpy as np
import os


def detect_events(input_file, output_file):
    # Read the events
    df = pd.read_csv(input_file)

    x = df["x"]
    y = df["y"]
    distances = np.sqrt(x**2 + y**2)

    # Tag events that fall within the unit circle centered at (0.5, 0.5) with radius 0.5
    df["detected"] = distances <= 1

    # Save the updated DataFrame
    df.to_csv(output_file, index=False)
    print(f"Tagged events saved to {output_file}")


if __name__ == "__main__":
    INPUT_FILE = "data/events.csv"
    OUTPUT_FILE = "data/detected_events.csv"

    detect_events(INPUT_FILE, OUTPUT_FILE)
