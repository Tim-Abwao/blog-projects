#!/usr/bin/python3
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib import ticker

df = pd.read_csv("comparison.csv", header=[0, 1], index_col=0)

# Customize matplotlib
plt.rc("figure", autolayout=True, dpi=95)
plt.rc("font", family="serif")
plt.rc("axes.spines", right=False, top=False)
plt.rc("axes", titlesize=11, titlepad=30, titlelocation="left")
plt.rc("lines", linewidth=2)
plt.rc("xtick", labelsize=8)
plt.rc("ytick", labelsize=8)

# Plot planning time
print("Plotting planning times.", end=" ")
plt.figure(figsize=(6, 3.3))
ax1 = sns.lineplot(
    data=df["plan"], palette=["silver", "lime"], dashes=False, legend=False
)
ax1.yaxis.set_major_formatter("{x:.2f}ms")
ax1.yaxis.set_major_locator(ticker.FixedLocator([0, 0.15, 0.3]))
ax1.set_xlabel("Run No.")
ax1.set_ylabel("Planning Time")
ax1.set_ylim([0, 0.38])
ax1.set_title(
    "The partitioned table took on average 0.17ms longer planning\n"
    "query execution."
)
for label, value in df["plan"].iloc[-1].items():
    ax1.text(16.2, value, f"{label} table")
for avg, line_color in zip(df["plan"].mean(), ["#bbb", "#afa"]):
    ax1.hlines(
        y=avg,
        xmin=1,
        xmax=16,
        linestyles="dashed",
        color=line_color,
        linewidth=1.5,
    )
    ax1.text(2, avg + 0.01, f"avg: {avg:.3f}", size=8, family="monospace")
plt.savefig("planning.png")
print("Done, saved as 'planning.png'.")

# Plot execution time
print("Plotting execution times.", end=" ")
plt.figure(figsize=(6, 3.4))
ax2 = sns.lineplot(
    data=df["exec"], palette=["silver", "lime"], dashes=False, legend=False
)
ax2.yaxis.set_major_formatter("{x:.0f}ms")
ax2.yaxis.set_major_locator(ticker.FixedLocator([0, 5, 10, 15]))
ax2.set_xlabel("Run No.")
ax2.set_ylabel("Execution Time")
ax2.set_ylim([0, 19])
ax2.set_title(
    "However, the partitioned table outperforms the normal one on\n"
    "query execution by 8.5ms on average. For a slight planning\n"
    "overhead, a signigficant speed boost is realized."
)
for label, value in df["exec"].iloc[-1].items():
    ax2.text(16.2, value, f"{label} table")
for avg, line_color in zip(df["exec"].mean(), ["#bbb", "#afa"]):
    ax2.hlines(
        y=avg,
        xmin=1,
        xmax=16,
        linestyles="dashed",
        color=line_color,
        linewidth=1.5,
    )
for avg, line_color in zip(df["exec"].mean(), ["#bbb", "#afa"]):
    ax2.hlines(
        y=avg,
        xmin=1,
        xmax=16,
        linestyles="dashed",
        color=line_color,
        linewidth=1.5,
    )
    ax2.text(5, avg + 0.5, f"avg: {avg:.3f}", size=8, family="monospace")
plt.savefig("executing.png")
print("Done, saved as 'executing.png'.")
