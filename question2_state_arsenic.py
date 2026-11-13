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

#-------------------------------------------------------------------------------------

# import pandas to organize the dataset
import pandas as pd

# import matplot to create graphs
import matplotlib.pyplot as plt

# Import ci-square test from SciPy
from scipy.stats import chi2_contingency

# Load the USGS groundwater dataset and skip the introduction
df=pd.read_csv(
    "arsenic_nov2001(ENGR 315 Project).csv",
    skiprows=[*range(58), 59]
    )

# Display the first 5 rows and colums to ensure it is loaded correctly
print (df. head())
print (df.columns)
print()

# Print the question: 
print ("How do arsenic concentrations in groundwater in different states compare to the EPA's drinking water standard?")

# Step 1: Indentify samples that exceed the standard-------------------------------

# Define the EPA standard in micrograms per liter
epa_limit = 10

# Select groundwater samples with arsenic concentrations greater than the standard
above_limit = df[df["AS_CONC"] > epa_limit]

# Print the total number of samples above the limit
print ("Total Groundwater Samples:", len(df))
print ("Samples Above the EPA Limit:", len(above_limit))
print()

# Step 2 : Compare arsenic concentrations between states------------------------------

# Create a neww column that shows whether a sample exceeds the limit
# True = Sample exceeds the limit / False = Sample does not exceed the limit
df["Above_EPA_Limit"] = df["AS_CONC"] > epa_limit

# Group the samples by state and perform calculations
state_results = df.groupby("STATE").agg(

    # Total number of samples 
    Total_Samples = ("AS_CONC", "count"),

    # Total nymber of samples exceeding the standard
    Samples_Above = ("Above_EPA_Limit", "sum"),

    # Average Arsenic Concentration
    Mean_Arsenic = ("AS_CONC", "mean"),
)

# Calculate the percentage of samples exceeding the limit per state
state_results["Percent_Above"] = (
    state_results["Samples_Above"]
    / state_results["Total_Samples"]
) * 100

# Sort states from highest to lowest percentage
state_results = state_results.sort_values(
    "Percent_Above", ascending = False
)

# Display Results
print("Arsenic Concentration by State:")
print(state_results)
print()

#Step 3: Graph the data -------------------------------------------------------------------

# Select top 10 states with highest percentage of samples that
# exceed the EPA drinking water standard
top_10 = state_results.head(10)

# Create a figure for the bar graph
plt.figure(figsize=(10,6))

# Plot the percentage
plt.bar(
    top_10.index,
    top_10["Percent_Above"]
)

# Inset a title and axis labels to organize the graph
plt.title ("Top 10 States Exceeding the EPA Arsenic Standard")
plt.xlabel("State")
plt.ylabel("Samples Above the EPA Standard (%)")

# Adjust layout
plt.tight_layout()

# Save the graph as a png file
plt.savefig("arsenic_state_graph.png", dpi=300)

# Display the graph
plt.show()

# Step 4: Check measurements-------------------------------------------------------------------

# Count measurement remarks in dataset
# This helps determine how arsenic values were reported
print("Arsenic Measurement Remarks")
print(df["AS_RMRK"].value_counts(dropna=False))
print()

# Check measurement remarks in samples
# Identify which measurement remarks appear with samples exceeding the limit
# because this helps determine whether th exceedance count includes measurements
# reported below the detection limit
print ("Measurement Remarks for Samples Above the EPA Limit:")
print(above_limit["AS_RMRK"].value_counts(dropna=False))
print()

# Investigate samples with the - remark
# Choose samples that have a - as their remark and display their concentration
dash_samples=df[df["AS_RMRK"] == "-"]

# Print the number of samples with this
print ("Samples with a - Remark", len(dash_samples))
print()

# Display the first 10 concentrations with this
print(dash_samples[["STATE","AS_RMRK", "AS_CONC"]].head(10))
print()

# Step 5: Summarize Results-----------------------------------------------------------------

# Display the 10 states with the highest percentages
print("Top 10 States by % that Exceed the EPA Limit")
print(state_results.head(10).round(2))
print()

# Calculate the overall percentage of samples above the EPA limit
overall_percent = (len(above_limit)/len(df))*100

# Display overall results
print("Overall Results:")
print("Total Samples:", len(df))
print("Samples Above the EPA Limit:", len(above_limit))
print("Percentage Above the EPA Limit:", round(overall_percent, 2), "%")
print()

# Save the state results for report
state_results.to_csv("arsenic_state_results.csv")

# Step 6: Perform a chi-square test-------------------------------------------------------------------

# Develop a table that shows how many samples are in each state are and are not above the standard
contingency_table = pd.crosstab(
    df["STATE"],
    df["Above_EPA_Limit"]
)

# Use a chi-square test to check whether arsenic levels exceeding the EPA standard vary between states
chi2, p_value, degrees_freedom, expected = chi2_contingency(
    contingency_table
)

# Display Results
print ("Chi-Square Test Results:")
print ("Statistic:", round(chi2,2))
print("P-Value:", p_value)
print("Degrees of Freedom:", degrees_freedom)
print()

# Check whether the expected counts are high enough for the test to be reliable
print ("Expected Counts Less than 5:", (expected<5).sum())
print()

# Use a significance level of 0.05
if p_value<0.05:
    print("Reject the null hypothesis")
    print("There is a statistically significant assosciation between  state and EPA exceedance status")
else:
    print("Fail to reject the null hypothesis")
    print("There is not enough significant evidence of an association between state and EPA exceedance status")

print()