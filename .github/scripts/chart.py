"""
Generate a beautiful donut chart from language stats.
Run: python chart.py
Output: language_chart.png
"""
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import numpy as np

# --- Data from README ---
languages = ["Python", "C#", "PowerShell", "Jupyter", "Shell", "Other"]
sizes     = [69.2, 19.8, 6.0, 1.6, 1.2, 2.2]
colors    = ["#3776AB", "#68217A", "#5391FE", "#F37726", "#4EAA25", "#95A5A6"]
explode   = (0.02, 0.02, 0.02, 0.02, 0.02, 0.02)

# --- Styling ---
plt.style.use("dark_background")
fig, ax = plt.subplots(figsize=(8, 8), facecolor="#0D1117")
ax.set_facecolor("#0D1117")

wedges, texts, autotexts = ax.pie(
    sizes,
    labels=None,
    autopct="%1.1f%%",
    startangle=200,
    pctdistance=0.78,
    colors=colors,
    explode=explode,
    wedgeprops={"width": 0.42, "edgecolor": "#0D1117", "linewidth": 2},
    textprops={"color": "white", "fontsize": 12, "fontweight": "bold"},
)

# --- Centre circle for donut ---
centre_circle = plt.Circle((0, 0), 0.52, fc="#0D1117", edgecolor="#30363D", linewidth=1.5)
ax.add_artist(centre_circle)

# --- Centre label ---
ax.text(0, 0.08, "Languages", ha="center", va="center", fontsize=16,
        fontweight="bold", color="white")
ax.text(0, -0.10, f"{len(languages)} total", ha="center", va="center", fontsize=11,
        color="#8B949E")

# --- Legend ---
legend_labels = [f"{lang}  ({sizes[i]}%)" for i, lang in enumerate(languages)]
ax.legend(
    wedges, legend_labels,
    title="Breakdown",
    loc="center left",
    bbox_to_anchor=(1, 0, 0.5, 1),
    labelcolor="white",
    facecolor="#161B22",
    edgecolor="#30363D",
    fontsize=10,
    title_fontsize=12,
)

# --- Title ---
ax.set_title("Juan José Solórzano — Code by Language", fontsize=18,
             fontweight="bold", color="white", pad=20)

plt.tight_layout()
plt.savefig("language_chart.png", dpi=200, bbox_inches="tight", facecolor="#0D1117")
plt.close()
print("✅ Chart saved → language_chart.png")
