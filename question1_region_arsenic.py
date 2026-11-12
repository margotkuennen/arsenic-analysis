# ENGR 315 - Arsenic Analysis
# Team: The Aquifers
# Group 22

# 1. How do arsenic concentrations in groundwater differ in urban and rural regions, 
# and how do these patterns relate to population density?


# Import necessary libraries 
import geopandas as gpd
import pandas as pd


# Load in the Arsenic Concentration data using geopandas
# Ignore any introductory comments in the data set (lines beginning with #)
arsenic_data = pd.read_csv(
    "arsenic_nov2001(ENGR 315 Project).csv",
    skiprows=[*range(58), 59]
)

# Check the available data in the Arsenic Concentrations of Groundwater file
print(arsenic_data.head())
print(arsenic_data.columns)
print(arsenic_data.shape)
print(arsenic_data.info())

# Load in the US Census data using geopandas
census_data = gpd.read_file("census_data_urban_areas/ua99_d00.shp")

census_data = census_data.set_crs("EPSG:4269")

# Check the available data in the 2000 US Census Urban Areas file
print(census_data.head())
print(census_data.columns)
print(census_data.crs)
print(census_data.shape)


