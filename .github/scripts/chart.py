"""
Generate a beautiful horizontal bar chart from language stats.
Uses seaborn for styling and matplotlib for customisation.
Run: python chart.py
Output: language_chart.png
"""
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

DATA_PCT_PATH = ".github/scripts/resources/data_pct.json"
PLOT_PATH = ".github/scripts/resources/language_chart.png"
# --- Data from README ---
with open(DATA_PCT_PATH,'r') as file:
    file_info = json.load(file)
languages = list(file_info.keys())
sizes = list(file_info.values())
#languages = ["Python", "C#", "PowerShell", "Jupyter", "Shell", "Other"]
#sizes     = [69.2, 19.8, 6.0, 1.6, 1.2, 2.2]

# Create a DataFrame for seaborn
df = pd.DataFrame({"Language": languages, "Percentage": sizes})
# Sort so the largest bar is at the top
df = df.sort_values("Percentage", ascending=True)

# --- Seaborn dark theme ---
sns.set_theme(style="darkgrid", rc={
    "figure.facecolor": "#0D1117",
    "axes.facecolor": "#0D1117",
    "text.color": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "#21262D",
})

fig, ax = plt.subplots(figsize=(10, 6))

# Create the horizontal bar chart (fix for seaborn v0.14+ deprecation)
palette = sns.color_palette("deep", len(languages))
bars = sns.barplot(
    data=df,
    y="Language",
    x="Percentage",
    hue="Language",          # assign y variable to hue to silence the warning
    palette=palette,
    legend=False,            # turn off redundant legend
    ax=ax,
    edgecolor="none",
    linewidth=0,
)

# Add percentage labels next to each bar
for bar, pct in zip(bars.patches, df["Percentage"]):
    width = bar.get_width()
    ax.text(
        width + 0.5,                 # slight offset from bar end
        bar.get_y() + bar.get_height() / 2,
        f"{pct:.1f}%",
        va="center",
        color="white",
        fontsize=11,
        fontweight="bold",
    )

# --- Styling touches ---
sns.despine(left=True, bottom=True)   # remove top/right/bottom spines
ax.tick_params(axis="y", length=0)    # no tick marks on y-axis
ax.grid(False, axis="y")              # no horizontal grid lines
ax.set_xlim(0, max(sizes) * 1.15)     # extra space for labels

# Labels and optional title
ax.set_xlabel("Percentage of Code", fontsize=13, color="white")
ax.set_ylabel("")
# ax.set_title("Language Distribution", fontsize=18, fontweight="bold", pad=20)

# --- Save the figure ---
plt.tight_layout()
plt.savefig(PLOT_PATH, dpi=200, bbox_inches="tight", facecolor="#0D1117")
plt.close()
print("✅ Chart saved → language_chart.png")