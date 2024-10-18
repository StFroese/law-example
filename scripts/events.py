import pandas as pd
import numpy as np
import os


def generate_events(n_points, output_file):
    # Generate random (x, y) points in the unit square [0, 1] x [0, 1]
    x = np.random.uniform(-1, 1, n_points)
    y = np.random.uniform(-1, 1, n_points)

    # Create a DataFrame
    df = pd.DataFrame({"x": x, "y": y})

    # Save to CSV
    df.to_csv(output_file, index=False)
    print(f"Generated {n_points} events and saved to {output_file}")


if __name__ == "__main__":
    # Number of points to generate
    N_POINTS = 10000
    OUTPUT_FILE = "data/events.csv"

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    generate_events(N_POINTS, OUTPUT_FILE)
