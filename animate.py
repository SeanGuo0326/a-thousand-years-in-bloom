# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

"""
A Thousand Years in Bloom — Timeline Animation

Each blossom represents one recorded year of
cherry blossom full bloom in Kyoto.

Animation structure:
1. Bloom — historical records appear from 812 to 2015
2. Hold — the complete thousand-year picture remains visible
3. Fall — all blossoms rotate and fall
4. Empty — a short pause
5. Loop — history begins again

Run:
    uv run animate.py
"""

import csv
import math
import random
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

def draw_flower(
    ax,
    x,
    y,
    size,
    color,
    alpha=0.9,
    rotation=0,
    mark_as_data=False
):

    for i in range(5):

        angle = i * 72 + rotation
        radians = math.radians(angle)

        px = (
            x
            + math.cos(radians)
            * size
            * 0.28
        )

        py = (
            y
            + math.sin(radians)
            * size
            * 0.28
        )

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

        if mark_as_data:
            petal._is_data_flower = True

        ax.add_patch(petal)

    centre = Circle(
        (x, y),
        radius=size * 0.12,
        facecolor="#f4c67a",
        edgecolor="none",
        alpha=alpha,
        zorder=4
    )

    if mark_as_data:
        centre._is_data_flower = True

    ax.add_patch(centre)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

records = rows(DATA)

if not records:
    raise ValueError(
        "No valid flowering records found."
    )

years = [
    record["year"]
    for record in records
]

flowering_days = [
    record["flowering_day"]
    for record in records
]

min_year = min(years)
max_year = max(years)

min_day = min(flowering_days)
max_day = max(flowering_days)

year_range = max(
    max_year - min_year,
    1
)

day_range = max(
    max_day - min_day,
    1
)

print(
    f"Loaded {len(records)} flowering records"
)

print(
    f"Years: {min_year} to {max_year}"
)

print(
    f"Flowering days: "
    f"{min_day} to {max_day}"
)


# --------------------------------------------------
# PREPARE FLOWER DATA
# --------------------------------------------------

# Fixed seed keeps the decorative falling motion
# consistent every time the program runs.

random.seed(42)

prepared_records = []

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


for record in records:

    year = record["year"]
    flowering_day = record["flowering_day"]

    # ----------------------------------------------
    # DATA → HORIZONTAL POSITION
    #
    # Earlier historical records appear on the left.
    # Later records appear on the right.
    # ----------------------------------------------

    x = (
        (year - min_year)
        / year_range
    ) * 84 + 10

    # ----------------------------------------------
    # DATA → VERTICAL POSITION
    #
    # Earlier flowering dates appear higher.
    # Later flowering dates appear lower.
    # ----------------------------------------------

    y = (
        1 -
        (flowering_day - min_day)
        / day_range
    ) * 60 + 18

    # ----------------------------------------------
    # DATA → COLOUR
    # ----------------------------------------------

    normalized_day = (
        (flowering_day - min_day)
        / day_range
    )

    color = (
        early_color
        * (1 - normalized_day)
        + late_color
        * normalized_day
    )

    # ----------------------------------------------
    # DECORATIVE FALL PARAMETERS
    #
    # These values DO NOT represent historical data.
    # They are used only to make the final transition
    # feel organic.
    # ----------------------------------------------

    fall_speed = random.uniform(
        0.88,
        1.18
    )

    drift = random.uniform(
        -7,
        7
    )

    sway = random.uniform(
        0.5,
        1.7
    )

    phase = random.uniform(
        0,
        math.tau
    )

    spin = random.uniform(
        -200,
        200
    )

    delay = random.uniform(
        0,
        0.15
    )

    prepared_records.append({
        "year": year,
        "flowering_day": flowering_day,
        "x": x,
        "y": y,
        "color": color,
        "fall_speed": fall_speed,
        "drift": drift,
        "sway": sway,
        "phase": phase,
        "spin": spin,
        "delay": delay
    })


# --------------------------------------------------
# CANVAS
# --------------------------------------------------

fig, ax = plt.subplots(
    figsize=(16, 9),
    facecolor="#101322"
)

ax.set_facecolor(
    "#101322"
)

ax.set_xlim(
    0,
    100
)

ax.set_ylim(
    0,
    100
)

ax.set_aspect(
    "equal",
    adjustable="box"
)

ax.axis(
    "off"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

ax.text(
    50,
    95,
    "A THOUSAND YEARS IN BLOOM",
    color="#ffe5ed",
    fontsize=25,
    ha="center",
    va="center"
)

ax.text(
    50,
    90,
    "Kyoto cherry blossom full-bloom records · 812–2015",
    color="#d8b8c9",
    fontsize=11,
    ha="center",
    va="center"
)


# --------------------------------------------------
# LEGEND
# --------------------------------------------------

draw_flower(
    ax,
    29,
    84,
    0.75,
    "#ff8eaa",
    alpha=0.95
)

ax.text(
    31,
    84,
    "Each blossom = one recorded year of full bloom",
    color="#d8b8c9",
    fontsize=9,
    ha="left",
    va="center"
)


# --------------------------------------------------
# VERTICAL DATA GUIDE
# --------------------------------------------------

ax.plot(
    [6, 6],
    [18, 78],
    color="#65596d",
    linewidth=0.8,
    alpha=0.7,
    zorder=1
)

ax.annotate(
    "",
    xy=(6, 79),
    xytext=(6, 76),
    arrowprops=dict(
        arrowstyle="->",
        color="#ff829e",
        linewidth=1
    )
)

ax.text(
    3.8,
    76,
    "EARLIER",
    color="#ff829e",
    fontsize=8,
    rotation=90,
    ha="center",
    va="center"
)

ax.text(
    3.8,
    22,
    "LATER",
    color="#f4c9d8",
    fontsize=8,
    rotation=90,
    ha="center",
    va="center"
)

ax.text(
    1.8,
    49,
    "FULL-BLOOM DATE",
    color="#8f8299",
    fontsize=7,
    rotation=90,
    ha="center",
    va="center"
)


# --------------------------------------------------
# HISTORICAL YEAR GUIDE
# --------------------------------------------------

for year in np.linspace(
    min_year,
    max_year,
    5
):

    x = (
        (year - min_year)
        / year_range
    ) * 84 + 10

    ax.text(
        x,
        13,
        str(int(year)),
        color="#766d80",
        fontsize=8,
        ha="center",
        va="center"
    )


# --------------------------------------------------
# CURRENT YEAR DISPLAY
# --------------------------------------------------

history_label = ax.text(
    50,
    8,
    "HISTORY IN BLOOM",
    color="#8f8299",
    fontsize=8,
    ha="center",
    va="center"
)

year_text = ax.text(
    50,
    4.5,
    str(min_year),
    color="#ffe5ed",
    fontsize=18,
    ha="center",
    va="center"
)


# --------------------------------------------------
# ANIMATION SETTINGS
# --------------------------------------------------

# Timeline growth
GROW_FRAMES = 150

# Pause at the completed 2015 visualisation
HOLD_FRAMES = 25

# Falling transition
FALL_FRAMES = 70

# Empty pause before restarting
EMPTY_FRAMES = 15

TOTAL_FRAMES = (
    GROW_FRAMES
    + HOLD_FRAMES
    + FALL_FRAMES
    + EMPTY_FRAMES
)

# Visual bloom duration.
# This is an animation timing parameter,
# not a biological measurement.

BLOOM_YEARS = 38

FULL_FLOWER_SIZE = 0.62
START_FLOWER_SIZE = 0.10


# --------------------------------------------------
# REMOVE ANIMATED FLOWERS
# --------------------------------------------------

def clear_data_flowers():

    animated_patches = [
        patch
        for patch in ax.patches
        if getattr(
            patch,
            "_is_data_flower",
            False
        )
    ]

    for patch in animated_patches:
        patch.remove()


# --------------------------------------------------
# BLOOM TIMELINE
# --------------------------------------------------

def draw_timeline(current_year):

    for record in prepared_records:

        if record["year"] > current_year:
            break

        age = (
            current_year
            - record["year"]
        )

        bloom_progress = (
            age
            / BLOOM_YEARS
        )

        bloom_progress = min(
            max(
                bloom_progress,
                0
            ),
            1
        )

        # Smoothstep easing:
        # small bud → opening → full blossom

        bloom_progress = (
            bloom_progress
            * bloom_progress
            * (
                3
                - 2 * bloom_progress
            )
        )

        size = (
            START_FLOWER_SIZE
            + (
                FULL_FLOWER_SIZE
                - START_FLOWER_SIZE
            )
            * bloom_progress
        )

        alpha = (
            0.35
            + 0.53
            * bloom_progress
        )

        draw_flower(
            ax,
            record["x"],
            record["y"],
            size,
            record["color"],
            alpha=alpha,
            rotation=0,
            mark_as_data=True
        )


# --------------------------------------------------
# FULL BLOOM
# --------------------------------------------------

def draw_full_bloom():

    for record in prepared_records:

        draw_flower(
            ax,
            record["x"],
            record["y"],
            FULL_FLOWER_SIZE,
            record["color"],
            alpha=0.88,
            rotation=0,
            mark_as_data=True
        )


# --------------------------------------------------
# FALLING FLOWERS
# --------------------------------------------------

def draw_falling(fall_frame):

    global_progress = (
        fall_frame
        / max(
            FALL_FRAMES - 1,
            1
        )
    )

    for record in prepared_records:

        # Each flower starts falling at a slightly
        # different moment.

        local_progress = (
            global_progress
            - record["delay"]
        )

        local_progress = (
            local_progress
            / (
                1
                - record["delay"]
            )
        )

        local_progress = min(
            max(
                local_progress,
                0
            ),
            1
        )

        # Accelerating downward movement

        fall_amount = (
            local_progress ** 1.6
        )

        # Vertical movement

        y = (
            record["y"]
            - 105
            * fall_amount
            * record["fall_speed"]
        )

        # Horizontal drift and gentle sway

        x = (
            record["x"]
            + record["drift"]
            * fall_amount
            + math.sin(
                local_progress
                * math.tau
                * 2
                + record["phase"]
            )
            * record["sway"]
        )

        # Rotation

        rotation = (
            record["spin"]
            * local_progress
        )

        # Gradually fade near the end

        alpha = (
            0.88
            * (
                1
                - local_progress ** 3
            )
        )

        # Slight size reduction

        size = (
            FULL_FLOWER_SIZE
            * (
                1
                - 0.10
                * local_progress
            )
        )

        # Skip flowers that have already
        # fallen below the canvas.

        if y < -5:
            continue

        draw_flower(
            ax,
            x,
            y,
            size,
            record["color"],
            alpha=alpha,
            rotation=rotation,
            mark_as_data=True
        )


# --------------------------------------------------
# MAIN ANIMATION
# --------------------------------------------------

def update(frame):

    clear_data_flowers()

    # ==============================================
    # PHASE 1 — BLOOM
    # ==============================================

    if frame < GROW_FRAMES:

        progress = (
            frame
            / max(
                GROW_FRAMES - 1,
                1
            )
        )

        current_year = (
            min_year
            + progress
            * year_range
        )

        history_label.set_text(
            "HISTORY IN BLOOM"
        )

        year_text.set_text(
            str(
                int(current_year)
            )
        )

        draw_timeline(
            current_year
        )

    # ==============================================
    # PHASE 2 — HOLD
    # ==============================================

    elif frame < (
        GROW_FRAMES
        + HOLD_FRAMES
    ):

        history_label.set_text(
            "A THOUSAND YEARS IN BLOOM"
        )

        year_text.set_text(
            str(max_year)
        )

        draw_full_bloom()

    # ==============================================
    # PHASE 3 — FALL
    # ==============================================

    elif frame < (
        GROW_FRAMES
        + HOLD_FRAMES
        + FALL_FRAMES
    ):

        fall_frame = (
            frame
            - GROW_FRAMES
            - HOLD_FRAMES
        )

        history_label.set_text(
            "SEASONS PASS"
        )

        year_text.set_text(
            ""
        )

        draw_falling(
            fall_frame
        )

    # ==============================================
    # PHASE 4 — EMPTY
    # ==============================================

    else:

        history_label.set_text(
            "HISTORY BEGINS AGAIN"
        )

        year_text.set_text(
            ""
        )


# --------------------------------------------------
# CREATE ANIMATION
# --------------------------------------------------

animation = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,

    # Slightly lower refresh frequency reduces
    # the rendering load when hundreds of flowers
    # are visible at the same time.
    interval=80,

    repeat=True,

    # Avoid storing every rendered frame in memory.
    cache_frame_data=False
)


# --------------------------------------------------
# SHOW
# --------------------------------------------------

plt.tight_layout()

plt.show()