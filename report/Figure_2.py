import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Load CSV data from GitHub
url = "https://raw.githubusercontent.com/hildahanyuwang/ECLAC/main/Adolescent%20birth%20rate%20(per%201000%20women).csv"
df = pd.read_csv(url)
print("Columns in the CSV:", df.columns.tolist())

# Filter rows for 10-14 years and convert values to numeric
df = df[df["Dim2"] == "10-14 years"]
df["First Tooltip"] = pd.to_numeric(df["First Tooltip"], errors="coerce")
df = df.dropna(subset=["First Tooltip"])

# Map countries
region_mapping = {
    # North America
    "Canada": "North America",
    "USA": "North America",
    # Europe & Central Asia
    "France": "Europe & Central Asia",
    "Germany": "Europe & Central Asia",
    "United Kingdom": "Europe & Central Asia",
    # East Asia & the Pacific
    "China": "East Asia & the Pacific",
    "Japan": "East Asia & the Pacific",
    "South Korea": "East Asia & the Pacific",
    # South Asia
    "India": "South Asia",
    "Pakistan": "South Asia",
    "Bangladesh": "South Asia",
    # Middle East & North Africa
    "Egypt": "Middle East & North Africa",
    "Saudi Arabia": "Middle East & North Africa",
    # Latin America & the Caribbean
    "Argentina": "Latin America & the Caribbean",
    "Barbados": "Latin America & the Caribbean",
    "Belize": "Latin America & the Caribbean",
    "Bolivia": "Latin America & the Caribbean",
    "Colombia": "Latin America & the Caribbean",
    "Costa Rica": "Latin America & the Caribbean",
    "Cuba": "Latin America & the Caribbean",
    "Dominican Republic": "Latin America & the Caribbean",
    "Ecuador": "Latin America & the Caribbean",
    "El Salvador": "Latin America & the Caribbean",
    "Guatemala": "Latin America & the Caribbean",
    "Guyana": "Latin America & the Caribbean",
    "Haiti": "Latin America & the Caribbean",
    "Honduras": "Latin America & the Caribbean",
    "Jamaica": "Latin America & the Caribbean",
    "Mexico": "Latin America & the Caribbean",
    "Paraguay": "Latin America & the Caribbean",
    "Peru": "Latin America & the Caribbean",
    "Saint Lucia": "Latin America & the Caribbean",
    "Suriname": "Latin America & the Caribbean",
    "Trinidad and Tobago": "Latin America & the Caribbean",
    # Sub-Saharan Africa
    "Nigeria": "Sub-Saharan Africa",
    "South Africa": "Sub-Saharan Africa",
    "Kenya": "Sub-Saharan Africa",
    "Ghana": "Sub-Saharan Africa"
}
df["Region"] = df["Location"].map(region_mapping).fillna("Other")


grouped = df.groupby("Region", as_index=False)["First Tooltip"].mean()

global_avg = df["First Tooltip"].mean()
world_avg_df = pd.DataFrame({'Region': ['World Average'], "First Tooltip": [global_avg]})
grouped = pd.concat([grouped, world_avg_df], ignore_index=True)

grouped = grouped.dropna(subset=["First Tooltip"])
grouped = grouped.sort_values("First Tooltip")
labels = grouped["Region"].tolist()
values = grouped["First Tooltip"].tolist()

# Function to split long region names into two lines
def split_label(label):
    if label == "Latin America & the Caribbean":
        return "Latin America &\nthe Caribbean"
    elif label == "East Asia & the Pacific":
        return "East Asia &\nthe Pacific"
    elif label == "Middle East & North Africa":
        return "Middle East &\nNorth Africa"
    elif label == "Sub-Saharan Africa":
        return "Sub-Saharan\nAfrica"
    elif label == "Europe & Central Asia":
        return "Europe &\nCentral Asia"
    else:
        return label

split_labels = [split_label(lab) for lab in labels]

fig, ax = plt.subplots(figsize=(8, 5), dpi=150)
bars = ax.bar(range(len(labels)), values, zorder=3)

for i, bar in enumerate(bars):
    region = labels[i]
    if region == "Latin America & the Caribbean":
        bar.set_color("#bf0637")
    else:
        bar.set_color("#3b4fbf")
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
            f"{int(round(bar.get_height()))}", ha="center", va="bottom",
            color="black", fontweight="bold", fontsize=10)

ax.set_title("Regional Adolescent Birth Rates (10-14 years)", fontsize=12, fontweight="bold")
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(split_labels, rotation=45, ha="right")
ax.set_xlim(-0.5, len(labels)-0.5)
ax.set_ylim(0, max(values) + 15)
ax.grid(axis="y", linestyle="-", linewidth=1.5, color="#ffffff", zorder=1)

yticks = ax.get_yticks()
for i in range(len(yticks) - 1):
    if i % 2 == 1:
        ax.axhspan(yticks[i], yticks[i+1], facecolor="#f6f8fb")

plt.tight_layout()
plt.show()
