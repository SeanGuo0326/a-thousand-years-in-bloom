# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

"""
A Thousand Years in Bloom — Animation Test

Iteration 2:
Historical cherry blossom records appear gradually
as time moves from 812 to 2015.

Run:
    uv run animate.py
"""

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.patches import Ellipse, Circle


# --------------------------------------------------
# FILE SETTINGS
# --------------------------------------------------

HERE = Path(__file__).parent
DATA = HERE / "data" / "SakuraData4.csv"


# --------------------------------------------------
# READ DATA
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

            records.append({
                "year": year,
                "flowering_day": flowering_day
            })

    return sorted(
        records,
        key=lambda record: record["year"]
    )


# --------------------------------------------------
# DRAW FLOWER
# --------------------------------------------------

def draw_flower(ax, x, y, size, color, alpha=0.9):

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
# LOAD DATA
# --------------------------------------------------

records = rows(DATA)

years = [record["year"] for record in records]
flowering_days = [
    record["flowering_day"]
    for record in records
]

min_year = min(years)
max_year = max(years)

min_day = min(flowering_days)
max_day = max(flowering_days)

year_range = max_year - min_year
day_range = max_day - min_day


# --------------------------------------------------
# CANVAS
# --------------------------------------------------

fig, ax = plt.subplots(
    figsize=(16, 9),
    facecolor="#101322"
)

ax.set_facecolor("#101322")

ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_aspect("equal", adjustable="box")
ax.axis("off")


# --------------------------------------------------
# STATIC TEXT
# --------------------------------------------------

ax.text(
    50,
    94,
    "A THOUSAND YEARS IN BLOOM",
    color="#ffe5ed",
    fontsize=25,
    fontweight="light",
    ha="center"
)

ax.text(
    50,
    88,
    "A visual history of Kyoto's cherry blossoms",
    color="#d8b8c9",
    fontsize=12,
    ha="center"
)


# Current year display
year_text = ax.text(
    50,
    7,
    str(min_year),
    color="#ffe5ed",
    fontsize=18,
    ha="center"
)


# --------------------------------------------------
# ANIMATION
# --------------------------------------------------

TOTAL_FRAMES = 180


def update(frame):

    # Remove flowers from previous frame
    for patch in list(ax.patches):
        patch.remove()

    progress = frame / (TOTAL_FRAMES - 1)

    current_year = (
        min_year
        + progress * year_range
    )

    year_text.set_text(
        str(int(current_year))
    )

    # Draw every record that has happened
    # up to the current historical year

    for record in records:

        if record["year"] > current_year:
            break

        year = record["year"]
        flowering_day = record["flowering_day"]

        x = (
            (year - min_year)
            / year_range
        ) * 90 + 5

        y = (
            1 -
            (flowering_day - min_day)
            / day_range
        ) * 68 + 16

        normalized_day = (
            (flowering_day - min_day)
            / day_range
        )

        early_color = np.array([
            0.98,
            0.38,
            0.55
        ])

        late_color = np.array([
            1.0,
            0.83,
            0.89
        ])

        color = (
            early_color * (1 - normalized_day)
            + late_color * normalized_day
        )

        draw_flower(
            ax,
            x,
            y,
            0.65,
            color,
            alpha=0.88
        )


animation = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    interval=50,
    repeat=True
)


plt.tight_layout()
plt.show()