# ENGR 315 - Arsenic Analysis
# Team: The Aquifiers
# Group 12

# Research Question 2
# How do arsenic concentrations in groundwater in different states 
# compare to the EPA's drinking water standard?

# Purpose:
# This progarm observes 

import pandas as pd
df=pd.read_csv(
    "arsenic_nov2001(ENGR 315 Project).csv",
    skiprows=[*range(58), 59]
    )


print (df. head())
print (df.columns)

