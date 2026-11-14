# ENGR 315 - Arsenic Analysis
# Team: The Aquifers
# Group 22

# 1. How do arsenic concentrations in groundwater differ in urban and rural regions, 
# and how do these patterns relate to population density?


# Import necessary libraries 
import geopandas as gpd
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt

### Step 1 - Load in datasets and organize them for direct comparison

# Load in the Arsenic Concentration data using geopandas
# Ignore any introductory comments in the data set (lines beginning with #)
arsenic_data = pd.read_csv(
    "arsenic_nov2001(ENGR 315 Project).csv",
    skiprows=[*range(58), 59]
)
# Remove extra spaces from column names
arsenic_data.columns = arsenic_data.columns.str.strip()
# Correct longitude values (Western Hemisphere)
arsenic_data["LON_DD"] = -arsenic_data["LON_DD"].abs()

# Use a GeoDataFrame for arsenic data
arsenic_points = gpd.GeoDataFrame(
    arsenic_data,
    geometry=gpd.points_from_xy(
        arsenic_data["LON_DD"], 
        arsenic_data["LAT_DD"]
    ), 
    crs="EPSG:4269"
)

# Check the available data in the Arsenic Concentrations of Groundwater file
#print(arsenic_data.head())
#print(arsenic_data.columns)
#print(arsenic_data.shape)
#print(arsenic_data.info())

# Load in the US Census data using geopandas
census_data = gpd.read_file("census_data_urban_areas/ua99_d00.shp")
census_data = census_data.set_crs("EPSG:4269")


# Check the available data in the 2000 US Census Urban Areas file
#print(census_data.head())
#print(census_data.columns)
#print(census_data.crs)
#print(census_data.shape)

### Step 2 - Sort each arsenic sample based on geographic location

# Perform a spatial join 
# Determine which arsenic samples are categorized as urban areas based on census data
arsenic_join = gpd.sjoin(
    arsenic_points,
    census_data,
    how="left",
    predicate="within"
)

# Categorize the arsenic samples as urban versus rural
# ASSUMPTION: non-urban areas will automatically be categorized as rural
arsenic_join["REGION"] = arsenic_join["NAME"].notna().map({
    True: "Urban",
    False: "Rural"
})

### Step 3 - Calculate metrics of sorted data samples

# Calculate statistics to compare arsenic concentrations in urban and rural areas
regional_stats = arsenic_join.groupby("REGION")["AS_CONC"].agg(
    ["count", "mean", "median", "std"]
)

# Print organized statistical data in the terminal
print("Arsenic Concentration Statistics by Region:")

regional_stats = regional_stats.rename(columns={
    "count": "Sample Count", 
    "mean": "Mean (ug/L)", 
    "median": "Median (ug/L)", 
    "std": "Std Dev (ug/L)"
})

print(regional_stats.to_string(float_format="{:.2f}".format))

### Step 4 - Conduct a two-sided T-test comparing urban and rural arsenic concentrations

# Extract urban and rural samples and store them separately
urban = arsenic_join[arsenic_join["REGION"] == "Urban"]["AS_CONC"].dropna()
rural = arsenic_join[arsenic_join["REGION"] == "Rural"]["AS_CONC"].dropna()

# Conduct the two-sided t-test
t_stat, p_value = stats.ttest_ind(
    urban, 
    rural, 
    equal_var=False
)

# Print the t-test results
print("Two-Sided T-Test:")
print("t-stat =", t_stat)
print("p-value =", p_value)

# Set a value for alpha
alpha = 0.05

# Determine whether to reject the null hypothesis
if p_value < alpha:
    print("Reject null hypothesis. The difference between urban and rural arsenic concentrations is significant.")
else:
    print("Fail to reject null hypothesis.")

### Step 5 - Create and display a data map of urban and rural arsenic concentrations

# Create map displaying sample locations
fig, ax = plt.subplots(figsize=(12, 8))

# Plot urban area boundaries (based on census data)
census_data.boundary.plot(
    ax=ax, 
    color = "lightgray",
    linewidth=0.3
)

# Plot urban groundwater samples
arsenic_join[arsenic_join["REGION"] == "Urban"].plot(
    ax=ax, 
    color="blue",
    markersize=5,
    alpha=0.6,
    label="Urban Samples"
)

# Plot rural groundwater samples
arsenic_join[arsenic_join["REGION"] == "Rural"].plot(
    ax=ax, 
    color="orange",
    markersize=5,
    alpha=0.6,
    label="Urban Samples"
)

# Title, labels, & legend for map
ax.set_title("Urban and Rural Groundwater Arsenic Sample Locations")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.legend()

plt.tight_layout()
# Adjust the scale 
ax.set_xlim(-180, -60)
ax.set_ylim(15, 72)

plt.show()
plt.savefig(
    r"C:\ENGR 315\arsenic-analysis\arsenic_region_map.png",
    dpi=300,
    bbox_inches="tight"
)