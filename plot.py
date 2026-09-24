
# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

"""
A Thousand Years in Bloom

A generative data visualisation of Kyoto cherry blossom
flowering dates from historical records.

Run:
    uv run plot.py

Output:
    out/plot.png
"""

import csv
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Circle


# --------------------------------------------------
# 1. FILE SETTINGS
# --------------------------------------------------

HERE = Path(__file__).parent

DATA = HERE / "data" / "SakuraData4.csv"
OUT = HERE / "out"

PICTURE = "plot.png"

random.seed(42)


# --------------------------------------------------
# 2. READ THE DATA
# --------------------------------------------------

def rows(path):

    records = []

    with path.open(
        encoding="utf-8-sig",
        newline=""
    ) as handle:

        reader = csv.DictReader(handle)

        for row in reader:

            year = row["year"].strip()
            flowering_day = row["flowering_day"].strip()

            if not year or not flowering_day:
                continue

            try:
                year = int(year)
                flowering_day = int(float(flowering_day))

            except ValueError:
                continue

            if not 1 <= flowering_day <= 366:
                continue

            records.append(
                {
                    "year": year,
                    "flowering_day": flowering_day
                }
            )

    return sorted(
        records,
        key=lambda record: record["year"]
    )


# --------------------------------------------------
# 3. DRAW A SAKURA FLOWER
# --------------------------------------------------

def draw_flower(ax, x, y, size, color, alpha=0.9):

    # Five petals
    for i in range(5):

        angle = i * 72

        radians = math.radians(angle)

        px = x + math.cos(radians) * size * 0.28
        py = y + math.sin(radians) * size * 0.28

        petal = Ellipse(
            (px, py),
            width=size * 0.78,
            height=size * 0.52,
            angle=angle,
            facecolor=color,
            edgecolor="none",
            alpha=alpha,
            zorder=3
        )

        ax.add_patch(petal)

    # Flower centre
    centre = Circle(
        (x, y),
        radius=size * 0.12,
        facecolor="#f4c67a",
        edgecolor="none",
        alpha=alpha,
        zorder=4
    )

    ax.add_patch(centre)


# --------------------------------------------------
# 4. MAIN VISUALISATION
# --------------------------------------------------

def main():

    records = rows(DATA)

    if not records:
        raise ValueError(
            "No valid flowering records found."
        )

    print(f"Loaded {len(records)} flowering records")

    years = [
        record["year"]
        for record in records
    ]

    flowering_days = [
        record["flowering_day"]
        for record in records
    ]

    print(
        f"Years: {min(years)} to {max(years)}"
    )

    print(
        f"Flowering days: "
        f"{min(flowering_days)} to {max(flowering_days)}"
    )

    # --------------------------------------------------
    # 5. CANVAS
    # --------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(16, 9),
        facecolor="#101322"
    )

    ax.set_facecolor("#101322")

    # Horizontal axis: historical year
    # Vertical axis: flowering day of the year

    min_year = min(years)
    max_year = max(years)

    min_day = min(flowering_days)
    max_day = max(flowering_days)

    year_range = max(max_year - min_year, 1)
    day_range = max(max_day - min_day, 1)

    # --------------------------------------------------
    # 6. BACKGROUND PARTICLES
    # --------------------------------------------------

    for _ in range(180):

        x = random.uniform(0, 100)
        y = random.uniform(0, 100)

        ax.scatter(
            x,
            y,
            s=random.uniform(1, 5),
            color="#f7c6d9",
            alpha=random.uniform(0.08, 0.3),
            linewidths=0,
            zorder=1
        )

    # --------------------------------------------------
    # 7. FLOWERING DATA
    # --------------------------------------------------

    for record in records:

        year = record["year"]
        flowering_day = record["flowering_day"]

        # Map year to horizontal position
        x = (
            (year - min_year)
            / year_range
        ) * 90 + 5

        # Map flowering day to vertical position
        # Earlier flowering appears higher

        y = (
            1 -
            (flowering_day - min_day)
            / day_range
        ) * 68 + 16

        # Colour represents flowering time
        # Earlier flowering: warmer pink
        # Later flowering: lighter pink

        normalized_day = (
            (flowering_day - min_day)
            / day_range
        )

        early_color = np.array(
            [0.98, 0.38, 0.55]
        )

        late_color = np.array(
            [1.0, 0.83, 0.89]
        )

        color = (
            early_color * (1 - normalized_day)
            + late_color * normalized_day
        )

        # Flower size
        size = 0.65

        draw_flower(
            ax,
            x,
            y,
            size,
            color,
            alpha=0.88
        )

    # --------------------------------------------------
    # 8. TITLE AND LABELS
    # --------------------------------------------------

    ax.text(
        50,
        94,
        "A THOUSAND YEARS IN BLOOM",
        color="#ffe5ed",
        fontsize=25,
        fontweight="light",
        ha="center",
        va="center"
    )

    ax.text(
        50,
        88,
        "A visual history of Kyoto's cherry blossoms",
        color="#d8b8c9",
        fontsize=12,
        ha="center",
        va="center"
    )

    # Year labels
    for year in np.linspace(
        min_year,
        max_year,
        5
    ):

        x = (
            (year - min_year)
            / year_range
        ) * 90 + 5

        ax.text(
            x,
            8,
            str(int(year)),
            color="#b7a8bc",
            fontsize=10,
            ha="center"
        )

    ax.text(
        50,
        3,
        "HISTORICAL YEAR",
        color="#b7a8bc",
        fontsize=10,
        ha="center"
    )

    ax.text(
        2,
        75,
        "EARLIER BLOOM",
        color="#ff829e",
        fontsize=9,
        rotation=90,
        va="center"
    )

    ax.text(
        2,
        20,
        "LATER BLOOM",
        color="#f4c9d8",
        fontsize=9,
        rotation=90,
        va="center"
    )

    # --------------------------------------------------
    # 9. FINAL LAYOUT
    # --------------------------------------------------

    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)

    ax.set_aspect("equal", adjustable="box")

    ax.axis("off")

    fig.tight_layout()

    # --------------------------------------------------
    # 10. SAVE THE PICTURE
    # --------------------------------------------------

    OUT.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = OUT / PICTURE

    fig.savefig(
        output_path,
        dpi=200,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight"
    )

    print(f"Saved: {output_path}")

    plt.show()


if __name__ == "__main__":
    main()