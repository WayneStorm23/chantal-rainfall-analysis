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

# Calculate cumulative rainfall
# Added 0.53" baseline from earlier rainfall already on gauge
df["cumulative"] = df["precip_in"].cumsum() + 0.53

# Calculate rolling 6-hour rainfall totals
# 24 rows × 15-minute observations = 6 hours
df["6hr_total"] = df["precip_in"].rolling(window=24).sum()

# Find wettest 6-hour period
idx = df["6hr_total"].idxmax()

peak = df.loc[idx, "6hr_total"]

# These timestamps are included in the rolling sum
window_start_timestamp = df.loc[idx - 23, "datetime"]
window_end = df.loc[idx, "datetime"]

# Actual rainfall window starts 15 minutes earlier
# because each timestamp represents rainfall during
# the PREVIOUS 15-minute interval
actual_window_start = (
    window_start_timestamp
    - pd.Timedelta(minutes=15)
)

# Plot style
plt.style.use("dark_background")

# Create figure
fig, ax = plt.subplots(
    figsize=(12, 6),
    facecolor="black"
)

# Plot cumulative rainfall line
ax.plot(
    df["datetime"],
    df["cumulative"],
    color="cyan",
    linewidth=3,
    zorder=2
)

# Highlight wettest 6-hour rainfall window
ax.axvspan(
    actual_window_start,
    window_end,
    color="gold",
    alpha=0.30,
    zorder=1
)

# Add annotation box
ax.text(
    actual_window_start +
    (window_end - actual_window_start) / 2,

    df["cumulative"].min() + 1,

    f'{peak:.2f}" in 6 hrs\n'
    f'({actual_window_start.strftime("%H:%M")}–'
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

# Grid styling
ax.grid(
    True,
    linestyle=":",
    color="gray",
    alpha=0.7,
    zorder=0
)

# Author credit
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
print(
    f"Wettest 6-hour total: "
    f"{peak:.2f} inches"
)

print(
    f"Timestamps summed: "
    f"{window_start_timestamp.strftime('%Y-%m-%d %H:%M')} "
    f"to "
    f"{window_end.strftime('%Y-%m-%d %H:%M')} EDT"
)

print(
    f"Actual rainfall window represented: "
    f"{actual_window_start.strftime('%Y-%m-%d %H:%M')} "
    f"to "
    f"{window_end.strftime('%Y-%m-%d %H:%M')} EDT"
)
