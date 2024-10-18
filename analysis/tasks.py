# coding: utf-8

"""
Location of tasks.
"""

import law
import luigi
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from pathlib import Path

law.contrib.load("pandas")


class AnalysisTask(law.Task):
    """
    Configure the base task to our needs
    """

    n_points = luigi.IntParameter(default=10000)

    def build_path(self):
        """Path to the build directory."""
        return Path(os.getenv("QS_DATA"))

    def local_target(self, path, *args):
        """Path to the local target."""
        return law.LocalFileTarget(self.build_path() / path, *args)


class GenerateEventsTask(AnalysisTask):
    """
    Task to generate random points within a square [-1, 1] x [-1, 1].
    """

    def output(self):
        return self.local_target("events.csv")

    def run(self):
        # Generate random (x, y) points
        x = np.random.uniform(-1, 1, self.n_points)
        y = np.random.uniform(-1, 1, self.n_points)

        # Create a DataFrame
        df = pd.DataFrame({"x": x, "y": y})

        # Save to CSV using PandasFormatter
        self.output().dump(df, formatter="dataframe")
        print(f"Generated {self.n_points} events and saved to {self.output().path}")


class DetectEventsTask(AnalysisTask):
    """
    Task to detect events that fall within the unit circle centered at (0, 0).
    """

    def requires(self):
        return GenerateEventsTask(self)

    def output(self):
        return self.local_target("events_detected.csv")

    def run(self):
        # Read the events using PandasFormatter
        df = self.input().load()

        # Calculate distance from the center (0, 0)
        distances = np.sqrt(df["x"] ** 2 + df["y"] ** 2)

        # Tag events that fall within the unit circle
        df["detected"] = distances <= 1.0

        # Save the updated DataFrame using PandasFormatter
        self.output().dump(df, formatter="dataframe")
        print(f"Tagged events saved to {self.output().path}")


class CalculatePiTask(AnalysisTask):
    """
    Task to calculate π based on the tagged events.
    """

    def requires(self):
        return DetectEventsTask(self)

    def output(self):
        return self.local_target("pi_estimate.txt")

    def run(self):
        df = self.input().load(formatter="dataframe")

        # Count the number of events inside the circle
        n_inside_circle = df["detected"].sum()
        n_total = len(df)

        # Estimate pi
        pi_estimate = (n_inside_circle / n_total) * 4

        # Save the estimated value of Pi
        self.output().dump(pi_estimate)

        print(f"Estimated Pi: {pi_estimate} (saved to {self.output().path})")


class PlotEventsTask(AnalysisTask):
    """
    Task to visualize the detection method by plotting the points.
    """

    def requires(self):
        return DetectEventsTask(self)

    def output(self):
        return self.local_target("plot_events.pdf")

    def run(self):
        df = self.input().load(formatter="dataframe")

        # Separate points inside and outside the circle
        inside_circle = df[df["detected"]]
        outside_circle = df[~df["detected"]]

        # Set up the figure
        fig, ax = plt.subplots(figsize=(8, 8))

        # Modern color palette using Matplotlib named colors
        inside_color = "dodgerblue"  # Modern blue
        outside_color = "coral"  # Modern orange-pink
        circle_color = "mediumseagreen"  # Modern green

        # Plotting the points
        ax.scatter(
            outside_circle["x"],
            outside_circle["y"],
            color=outside_color,
            s=10,
            alpha=0.6,
            label="Outside Circle",
        )
        ax.scatter(
            inside_circle["x"],
            inside_circle["y"],
            color=inside_color,
            s=10,
            alpha=0.6,
            label="Inside Circle",
        )

        # Draw circle for reference
        circle = plt.Circle(
            (0, 0),
            1.0,
            edgecolor=circle_color,
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
        plt.savefig(self.output().path, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"Plot saved to {self.output().path}")
