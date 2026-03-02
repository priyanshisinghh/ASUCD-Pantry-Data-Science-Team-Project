import pandas as pd
from scipy.stats import spearmanr
df = pd.read_csv('cleanq2data.csv')

#run spearman correlation on cleaned data
rho, p_value = spearmanr(df['satisfaction_rating'], df['items_grabbed_ordinal'])

#print results
print(f"Correlation Coefficient: {rho}")
print(f"P-value: {p_value}")