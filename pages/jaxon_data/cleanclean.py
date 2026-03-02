import pandas as pd
df = pd.read_csv('c1pantryresponsedata.csv')

# target columns 
satisfaction_col = 'Rate your satisfaction of the item selection'
items_grabbed_col = 'How many unique items do you roughly grab while at the Pantry?'

# Drop empty rows
cleaned_df = df[[satisfaction_col, items_grabbed_col]].dropna().copy()

# Map options to numbers
itemmap = {
    '1-2 different items': 1,
    '3-5 different items': 2,
    '6-10 different items': 3,
    '10+ different items': 4
}
# rename rate you satisfaction to satisfaction_rating
cleaned_df = cleaned_df.rename(columns={satisfaction_col: 'satisfaction_rating'})
cleaned_df['items_grabbed_ordinal'] = cleaned_df[items_grabbed_col].map(itemmap)

#Export
cleaned_df.to_csv('cleanq2data.csv', index=False)
print("Cleaned")