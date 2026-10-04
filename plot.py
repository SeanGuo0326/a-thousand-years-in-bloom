# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

"""
A Thousand Years in Bloom — Final Static Visualisation

Each blossom represents one recorded year of
cherry blossom full bloom in Kyoto.

Data mapping:
- Year -> horizontal position
- Full-bloom date -> vertical position
- Full-bloom date -> blossom colour

Output:
    out/plot.png

Run:
    uv run plot.py
"""

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path as MarkerPath


# --------------------------------------------------
# FILE SETTINGS
# --------------------------------------------------

HERE = Path(__file__).parent
DATA = HERE / "data" / "SakuraData4.csv"

OUTPUT_DIR = HERE / "out"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_PATH = OUTPUT_DIR / "plot.png"


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
# MAIN
# --------------------------------------------------

def main():

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
    # DATA -> HORIZONTAL POSITION
    # --------------------------------------------------

    x = (
        (years - min_year)
        / year_range
    ) * 84 + 10


    # --------------------------------------------------
    # DATA -> VERTICAL POSITION
    #
    # Earlier flowering dates appear higher.
    # Later flowering dates appear lower.
    # --------------------------------------------------

    y = (
        1
        - (
            flowering_days - min_day
        )
        / day_range
    ) * 60 + 18


    # --------------------------------------------------
    # DATA -> COLOUR
    # --------------------------------------------------

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


    # Add alpha channel.

    colors = np.column_stack(
        (
            rgb_colors,
            np.full(
                len(records),
                0.88
            )
        )
    )


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
    # DATA FLOWERS
    # --------------------------------------------------

    ax.scatter(
        x,
        y,
        s=np.full(
            len(records),
            30
        ),
        marker=FLOWER_MARKER,
        c=colors,
        edgecolors="none",
        zorder=3
    )


    # --------------------------------------------------
    # FINAL STATE LABEL
    # --------------------------------------------------

    ax.text(
        50,
        8,
        "A THOUSAND YEARS IN BLOOM",
        color="#8f8299",
        fontsize=8,
        ha="center",
        va="center"
    )


    ax.text(
        50,
        4.5,
        str(max_year),
        color="#ffe5ed",
        fontsize=18,
        ha="center",
        va="center"
    )


    # --------------------------------------------------
    # SAVE
    # --------------------------------------------------

    plt.tight_layout()


    fig.savefig(
        OUTPUT_PATH,
        dpi=180,
        facecolor=fig.get_facecolor(),
        bbox_inches="tight"
    )


    print("")
    print(
        f"Saved final visualisation to: {OUTPUT_PATH}"
    )
    print("")


    plt.show()


# --------------------------------------------------
# RUN
# --------------------------------------------------

if __name__ == "__main__":
    main()