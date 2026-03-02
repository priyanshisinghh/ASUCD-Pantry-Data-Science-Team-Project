import pandas as pd
from scipy.stats import chi2_contingency

# Race
race_table = pd.crosstab(df_clean['race'], df_clean['rare_never'])
chi2_race, p_race, dof_race, expected_race = chi2_contingency(race_table)

# Asian vs Non-Asian
asian_table = pd.crosstab(df_clean['asian_label'], df_clean['rare_never'])
chi2_asian, p_asian, dof_asian, expected_asian = chi2_contingency(asian_table)

# Ethnicity
eth_table = pd.crosstab(df_clean['ethnicity'], df_clean['rare_never'])
chi2_eth, p_eth, dof_eth, expected_eth = chi2_contingency(eth_table)
