import pandas as pd
from scipy.stats import chi2_contingency
df = pd.read_csv('cleanq1data.csv')

# Contingency table
contingency_table = pd.crosstab(df.iloc[:, 0], df.iloc[:, 1])

print("Contingency Table")
# transpose table (role column and method row)
print(contingency_table.T)
print("\n")


# run chi-square test
chi2, p, dof, expected = chi2_contingency(contingency_table)

# print results
print(f"Chi-Squared: {chi2}")
print(f"P-value: {p}")
print(f"Degrees of Freedom: {dof}")

