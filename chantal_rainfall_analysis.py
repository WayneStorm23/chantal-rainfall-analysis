"""

Tropical Storm Chantal Rainfall Analysis
Wayne Morley

"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Read CSV file
df = pd.read_csv(
    "usgs_precip_data.csv",
    parse_dates=["datetime"]
)

# Cumulative rainfall
# Includes 0.53" already in the gauge before the main event
df["cumulative"] = df["precip_in"].cumsum() + 0.53

# Rolling 6-hour rainfall totals
df["6hr_total"] = df["precip_in"].rolling(window=24).sum()

# Wettest 6-hour rainfall window
idx = df["6hr_total"].idxmax()

peak = df.loc[idx, "6hr_total"]

window_start = (
    df.loc[idx - 23, "datetime"]
    - pd.Timedelta(minutes=15)
)
window_end = df.loc[idx, "datetime"]

# Plot setup
plt.style.use("dark_background")

fig, ax = plt.subplots(
    figsize=(12, 6),
    facecolor="black"
)

# Plot cumulative rainfall
ax.plot(
    df["datetime"],
    df["cumulative"],
    color="cyan",
    linewidth=3,
    zorder=2
)

# Highlight wettest 6-hour window
ax.axvspan(
    window_start,
    window_end,
    color="gold",
    alpha=0.30,
    zorder=1
)

# Annotation
ax.text(
    window_start + (window_end - window_start) / 2,
    df["cumulative"].min() + 1,

    f'{peak:.2f}" in 6 hrs\n'
    f'({window_start.strftime("%H:%M")}–'
    f'{window_end.strftime("%H:%M")} EDT)',

    ha="center",
    va="bottom",
    color="white",
    fontsize=12,
    weight="bold",

    bbox=dict(
        facecolor="black",
        alpha=0.65,
        pad=5
    )
)

# X-axis range
ax.set_xlim(
    df["datetime"].min(),
    pd.Timestamp("2025-07-07 06:30")
)

# Styling
ax.set_facecolor("black")

for spine in ax.spines.values():
    spine.set_color("white")

ax.tick_params(
    colors="white",
    labelsize=11
)

ax.xaxis.set_major_formatter(
    mdates.DateFormatter("%m-%d %H:%M")
)

fig.autofmt_xdate(rotation=30)

# Labels and title
ax.set_xlabel(
    "Time (EDT)",
    color="white",
    fontsize=14
)

ax.set_ylabel(
    "Cumulative Precipitation (inches)",
    color="white",
    fontsize=14
)

ax.set_title(
    "Rain gauge at Bolin Creek Village Drive at Chapel Hill NC",
    color="white",
    fontsize=16,
    pad=15
)

# Grid
ax.grid(
    True,
    linestyle=":",
    color="gray",
    alpha=0.7,
    zorder=0
)

# Credit
fig.text(
    0.02,
    0.98,
    "Graph by Wayne",
    fontsize=9,
    color="white",
    ha="left",
    va="top"
)

# Final layout
plt.tight_layout()

# Display graph
plt.show()

# Verification output
print(f"Wettest 6-hour total: {peak:.2f} inches")

print(
    f"Wettest rainfall window: "
    f"{window_start.strftime('%Y-%m-%d %H:%M')} "
    f"to "
    f"{window_end.strftime('%Y-%m-%d %H:%M')} EDT"
)
