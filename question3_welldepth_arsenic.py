# Research Question 3
# Is there a geographic connection between well-depth and arsenic concentrations?

# Purpose:
# This program checks if well depth is associated with arsenic concentrations in groundwater. Using the WELLDPTH
# (well depth) and AS_CONC (arsenic concentration) columns, it performs linear regression and makes a scatterplot
# to visualize the trend. The data is also split into East and West regions (using longitude) so the regression
# results can be compared between the two halves of the country.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv(
    "arsenic_nov2001(ENGR 315 Project).csv",
    skiprows=[*range(58), 59]  # skip introduction lines
)

# strip extra lines out to clean data
df.columns = df.columns.str.strip()

print(df.head())
print(df.columns)
print()

# Step 1: Clean the data

# convert columns to numbers
df["WELLDPTH"] = pd.to_numeric(df["WELLDPTH"], errors="coerce")
df["AS_CONC"] = pd.to_numeric(df["AS_CONC"], errors="coerce")

# get rid of rows missing well depth or concentration
clean = df.dropna(subset=["WELLDPTH", "AS_CONC"]).copy()

print("Total groundwater samples:", len(df))
print("Samples with complete well depth and concentration:", len(clean))
print()

# Step 2: Look at samples reported below the detection limit

below = clean[clean["AS_RMRK"] == "<"]
above = clean[clean["AS_RMRK"] != "<"]

print("Samples reported below the detection limit (<):", len(below))
print("Samples reported at or above the detection limit:", len(above))
print()

# Step 3: Do linear regression

def get_regression(x, y):
    x_mean = x.mean()
    y_mean = y.mean()

    dx = x - x_mean
    dy = y - y_mean

    slope = (dx * dy).sum() / (dx * dx).sum()
    intercept = y_mean - slope * x_mean

    r = (dx * dy).sum() / np.sqrt((dx * dx).sum() * (dy * dy).sum())
    r2 = r * r

    return slope, intercept, r, r2

slope, intercept, r, r2 = get_regression(clean["WELLDPTH"], clean["AS_CONC"])

print("Full Dataset Linear Regression:")
print("Slope:", round(slope, 6))
print("Intercept:", round(intercept, 4))
print("Correlation coefficient (r):", round(r, 6))
print("R-squared:", round(r2, 6))
print()

# Step 4: Split into East and West regions and compare

# bigger number = further west
west = clean[clean["LON_DD"] > 100]
east = clean[clean["LON_DD"] <= 100]

print("West region samples:", len(west))
print("East region samples:", len(east))
print()

west_slope, west_int, west_r, west_r2 = get_regression(west["WELLDPTH"], west["AS_CONC"])
east_slope, east_int, east_r, east_r2 = get_regression(east["WELLDPTH"], east["AS_CONC"])

print("West Region Linear Regression:")
print("Slope:", round(west_slope, 6))
print("Intercept:", round(west_int, 4))
print("R-squared:", round(west_r2, 6))
print()

print("East Region Linear Regression:")
print("Slope:", round(east_slope, 6))
print("Intercept:", round(east_int, 4))
print("R-squared:", round(east_r2, 6))
print()

# Step 5: Make a scatterplot of well depth vs arsenic concentration

# get points
x_line = np.linspace(clean["WELLDPTH"].min(), clean["WELLDPTH"].max(), 100)
y_line = slope * x_line + intercept

plt.figure(figsize=(10, 6))

plt.scatter(clean["WELLDPTH"], clean["AS_CONC"], alpha=0.4, label="Sample")
plt.plot(x_line, y_line, color="red", label="Best fit")

plt.title("Well Depth vs Arsenic Concentration")
plt.xlabel("Well Depth (feet)")
plt.ylabel("Arsenic Concentration (ug/L)")

plt.legend()
plt.tight_layout()

plt.savefig("arsenic_well_depth_scatter.png", dpi=300)

# show finished plot
plt.show()