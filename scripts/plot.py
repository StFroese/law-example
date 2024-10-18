import pandas as pd
import matplotlib.pyplot as plt
import os


def plot_events(input_file, output_file):
    # Read the detected events
    df = pd.read_csv(input_file)

    # Separate points inside and outside the circle
    inside_circle = df[df["detected"]]
    outside_circle = df[~df["detected"]]

    # Set up the figure
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plotting the points
    ax.scatter(
        outside_circle["x"],
        outside_circle["y"],
        color="coral",
        s=10,
        alpha=0.5,
        label="Outside Circle",
    )
    ax.scatter(
        inside_circle["x"],
        inside_circle["y"],
        color="dodgerblue",
        s=10,
        alpha=0.5,
        label="Inside Circle",
    )

    # Draw circle for reference
    circle = plt.Circle(
        (0, 0),
        1.0,
        edgecolor="mediumseagreen",
        facecolor="none",
        linewidth=2,
        linestyle="--",
        label="Unit Circle",
    )
    ax.add_artist(circle)

    # Set axis limits and aspect ratio
    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal", "box")

    # Improve labels and title
    ax.set_title("Monte Carlo Estimation of π", fontsize=16, pad=20)
    ax.set_xlabel("X Coordinate", fontsize=14)
    ax.set_ylabel("Y Coordinate", fontsize=14)

    # Customize ticks
    ax.tick_params(axis="both", which="major", labelsize=12)

    # Remove top and right spines
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    # Add gridlines
    ax.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)

    # Improve legend
    legend = ax.legend(loc="upper right", fontsize=12, frameon=True)
    legend.get_frame().set_edgecolor("black")
    legend.get_frame().set_facecolor("white")
    legend.get_frame().set_alpha(0.9)

    # Add annotation with estimated π
    n_inside_circle = len(inside_circle)
    n_total = len(df)
    pi_estimate = (n_inside_circle / n_total) * 4
    annotation_text = f"Estimated π ≈ {pi_estimate:.6f}"
    ax.text(-1.0, -1.2, annotation_text, fontsize=14, ha="left")

    # Save the plot with high resolution
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Plot saved to {output_file}")


if __name__ == "__main__":
    INPUT_FILE = "data/detected_events.csv"
    OUTPUT_FILE = "data/pi_estimation_plot.pdf"

    plot_events(INPUT_FILE, OUTPUT_FILE)
