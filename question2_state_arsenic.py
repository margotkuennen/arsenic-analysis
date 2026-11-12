# ENGR 315 - Arsenic Analysis
# Team: The Aquifiers
# Group 12

# Research Question 2
# How do arsenic concentrations in groundwater in different states 
# compare to the EPA's drinking water standard?

# Purpose:
# This progarm observes groundwater arsenic concentrations accross different
# states in the U.S. We will compare these concentration values with the EPA
# drinking water standard of 10 micrograms per liter (ug/L). We will calculate
# the number and % of samples above the standard per state then use a graph to 
# compare results

# import pandas to organize the dataset
import pandas as pd

# Load the USGS groundwater dataset and skip the introduction
df=pd.read_csv(
    "arsenic_nov2001(ENGR 315 Project).csv",
    skiprows=[*range(58), 59]
    )

# Display the first 5 rows and colums to ensure it is loaded correctly
print (df. head())
print (df.columns)

