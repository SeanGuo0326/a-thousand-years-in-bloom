# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy", "pillow"]
# ///

"""
A Thousand Years in Bloom — Optimised Timeline Animation

Each blossom represents one recorded year of
cherry blossom full bloom in Kyoto.

Data mapping:
- Year -> horizontal position
- Full-bloom date -> vertical position and colour

Animation:
1. Historical records bloom from 812 to 2015
2. The complete dataset remains visible
3. Blossoms fall away
4. The animation restarts

Performance optimisation:
Instead of creating thousands of individual
Ellipse patches every frame, blossoms are rendered
with one reusable scatter collection.

Output:
    out/bloom-animation.gif

Run:
    uv run animate.py
"""

import csv
import math
import random
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter
from matplotlib.path import Path as MarkerPath


# --------------------------------------------------
# FILE SETTINGS
# --------------------------------------------------

HERE = Path(__file__).parent
DATA = HERE / "data" / "SakuraData4.csv"

OUTPUT_DIR = HERE / "out"
OUTPUT_DIR.mkdir(exist_ok=True)

GIF_PATH = OUTPUT_DIR / "bloom-animation.gif"


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
# CREATE FIVE-PETAL FLOWER MARKER
# --------------------------------------------------

def flower_marker():

    vertices = []
    codes = []

    points = 100

    for i in range(points + 1):

        theta = (
            i
            / points
            * math.tau
        )

        radius = (
            0.72
            + 0.28
            * math.cos(
                5 * theta
            )
        )

        x = (
            radius
            * math.cos(theta)
        )

        y = (
            radius
            * math.sin(theta)
        )

        vertices.append(
            (x, y)
        )

        if i == 0:
            codes.append(
                MarkerPath.MOVETO
            )
        else:
            codes.append(
                MarkerPath.LINETO
            )

    vertices.append(
        vertices[0]
    )

    codes.append(
        MarkerPath.CLOSEPOLY
    )

    return MarkerPath(
        vertices,
        codes
    )


FLOWER_MARKER = flower_marker()


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

records = rows(DATA)

if not records:
    raise ValueError(
        "No valid flowering records found."
    )


years = np.array([
    record["year"]
    for record in records
], dtype=float)


flowering_days = np.array([
    record["flowering_day"]
    for record in records
], dtype=float)


min_year = int(
    years.min()
)

max_year = int(
    years.max()
)

min_day = int(
    flowering_days.min()
)

max_day = int(
    flowering_days.max()
)


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
    f"Flowering days: {min_day} to {max_day}"
)


# --------------------------------------------------
# DATA MAPPING
# --------------------------------------------------

# Historical year -> horizontal position

base_x = (
    (years - min_year)
    / year_range
) * 84 + 10


# Full-bloom date -> vertical position
# Earlier dates appear higher.

base_y = (
    1
    - (
        flowering_days - min_day
    )
    / day_range
) * 60 + 18


# Full-bloom date -> colour

normalized_day = (
    flowering_days - min_day
) / day_range


early_color = np.array([
    0.98,
    0.38,
    0.55
])


late_color = np.array([
    1.00,
    0.83,
    0.89
])


rgb_colors = (
    early_color[None, :]
    * (
        1
        - normalized_day[:, None]
    )
    + late_color[None, :]
    * normalized_day[:, None]
)


# --------------------------------------------------
# FALLING PARAMETERS
# --------------------------------------------------

# These parameters are decorative.
# They do NOT represent historical data.

random.seed(42)

count = len(records)


fall_speed = np.array([
    random.uniform(
        0.88,
        1.18
    )
    for _ in range(count)
])


drift = np.array([
    random.uniform(
        -7,
        7
    )
    for _ in range(count)
])


sway = np.array([
    random.uniform(
        0.5,
        1.7
    )
    for _ in range(count)
])


phase = np.array([
    random.uniform(
        0,
        math.tau
    )
    for _ in range(count)
])


delay = np.array([
    random.uniform(
        0,
        0.15
    )
    for _ in range(count)
])


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

ax.scatter(
    [29],
    [84],
    s=[55],
    marker=FLOWER_MARKER,
    c=["#ff8eaa"],
    edgecolors="none",
    zorder=3
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

for guide_year in np.linspace(
    min_year,
    max_year,
    5
):

    guide_x = (
        (guide_year - min_year)
        / year_range
    ) * 84 + 10

    ax.text(
        guide_x,
        13,
        str(int(guide_year)),
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
# ANIMATED FLOWER COLLECTION
# --------------------------------------------------

initial_offsets = np.column_stack(
    (
        base_x,
        base_y
    )
)


initial_sizes = np.zeros(
    count
)


initial_colors = np.column_stack(
    (
        rgb_colors,
        np.zeros(count)
    )
)


# All flowers are contained inside ONE
# reusable scatter collection.

flowers = ax.scatter(
    base_x,
    base_y,
    s=initial_sizes,
    marker=FLOWER_MARKER,
    c=initial_colors,
    edgecolors="none",
    zorder=3
)


# --------------------------------------------------
# ANIMATION SETTINGS
# --------------------------------------------------

# Historical timeline

GROW_FRAMES = 150


# Complete dataset pause

HOLD_FRAMES = 25


# Falling animation

FALL_FRAMES = 70


# Empty pause before restart

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


# Scatter marker size uses points squared.

FULL_FLOWER_SIZE = 30

START_FLOWER_SIZE = 1


# --------------------------------------------------
# HIDE FLOWERS
# --------------------------------------------------

def hide_flowers():

    flowers.set_sizes(
        np.zeros(count)
    )

    hidden_colors = np.column_stack(
        (
            rgb_colors,
            np.zeros(count)
        )
    )

    flowers.set_facecolors(
        hidden_colors
    )


# --------------------------------------------------
# PHASE 1 — TIMELINE BLOOM
# --------------------------------------------------

def update_bloom(current_year):

    age = (
        current_year
        - years
    )


    visible = (
        age >= 0
    )


    bloom_progress = (
        age
        / BLOOM_YEARS
    )


    bloom_progress = np.clip(
        bloom_progress,
        0,
        1
    )


    # Smoothstep easing:
    # small bud -> opening -> full blossom

    bloom_progress = (
        bloom_progress
        * bloom_progress
        * (
            3
            - 2 * bloom_progress
        )
    )


    sizes = (
        START_FLOWER_SIZE
        + (
            FULL_FLOWER_SIZE
            - START_FLOWER_SIZE
        )
        * bloom_progress
    )


    sizes = np.where(
        visible,
        sizes,
        0
    )


    alpha = (
        0.35
        + 0.53
        * bloom_progress
    )


    alpha = np.where(
        visible,
        alpha,
        0
    )


    colors = np.column_stack(
        (
            rgb_colors,
            alpha
        )
    )


    flowers.set_offsets(
        initial_offsets
    )

    flowers.set_sizes(
        sizes
    )

    flowers.set_facecolors(
        colors
    )


# --------------------------------------------------
# PHASE 2 — FULL BLOOM
# --------------------------------------------------

def update_full_bloom():

    flowers.set_offsets(
        initial_offsets
    )


    flowers.set_sizes(
        np.full(
            count,
            FULL_FLOWER_SIZE
        )
    )


    colors = np.column_stack(
        (
            rgb_colors,
            np.full(
                count,
                0.88
            )
        )
    )


    flowers.set_facecolors(
        colors
    )


# --------------------------------------------------
# PHASE 3 — FALLING FLOWERS
# --------------------------------------------------

def update_fall(fall_frame):

    global_progress = (
        fall_frame
        / max(
            FALL_FRAMES - 1,
            1
        )
    )


    # Individual start delays

    local_progress = (
        global_progress
        - delay
    )


    local_progress = (
        local_progress
        / (
            1
            - delay
        )
    )


    local_progress = np.clip(
        local_progress,
        0,
        1
    )


    # Accelerating fall

    fall_amount = (
        local_progress ** 1.6
    )


    # Vertical movement

    current_y = (
        base_y
        - 105
        * fall_amount
        * fall_speed
    )


    # --------------------------------------------------
    # CONTINUOUS HORIZONTAL MOVEMENT
    #
    # Subtracting sin(phase) makes the horizontal
    # displacement start at exactly zero.
    #
    # This prevents flowers from jumping sideways
    # when the animation changes from HOLD to FALL.
    # --------------------------------------------------

    sway_motion = (
        (
            np.sin(
                local_progress
                * math.tau
                * 2
                + phase
            )
            - np.sin(phase)
        )
        * sway
        * local_progress
    )


    current_x = (
        base_x
        + drift
        * fall_amount
        + sway_motion
    )


    offsets = np.column_stack(
        (
            current_x,
            current_y
        )
    )


    # Fade flowers near the end

    alpha = (
        0.88
        * (
            1
            - local_progress ** 3
        )
    )


    alpha = np.where(
        current_y < -5,
        0,
        alpha
    )


    # Slight size reduction

    sizes = (
        FULL_FLOWER_SIZE
        * (
            1
            - 0.10
            * local_progress
        )
    )


    sizes = np.where(
        current_y < -5,
        0,
        sizes
    )


    colors = np.column_stack(
        (
            rgb_colors,
            alpha
        )
    )


    flowers.set_offsets(
        offsets
    )

    flowers.set_sizes(
        sizes
    )

    flowers.set_facecolors(
        colors
    )


# --------------------------------------------------
# MAIN ANIMATION
# --------------------------------------------------

def update(frame):

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


        update_bloom(
            current_year
        )


    # ==============================================
    # PHASE 2 — FULL BLOOM / HOLD
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


        update_full_bloom()


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


        update_fall(
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


        hide_flowers()


    return (
        flowers,
        history_label,
        year_text
    )


# --------------------------------------------------
# CREATE ANIMATION
# --------------------------------------------------

animation = FuncAnimation(
    fig,
    update,
    frames=TOTAL_FRAMES,
    interval=50,
    repeat=True,
    cache_frame_data=False
)


# --------------------------------------------------
# EXPORT GIF
# --------------------------------------------------

plt.tight_layout()

print("")
print("Exporting final animation...")
print("Please wait. Do not close the terminal.")

animation.save(
    GIF_PATH,
    writer=PillowWriter(
        fps=20
    ),

    # Lower export DPI keeps the GIF practical
    # for viewing directly on GitHub.
    dpi=90
)

print("")
print(
    f"Saved animation to: {GIF_PATH}"
)
print("")


# --------------------------------------------------
# SHOW
# --------------------------------------------------

plt.show()