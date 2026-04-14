#import os
import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency, spearmanr


#Folder next to this script
#_folder = os.path.dirname(os.path.abspath(__file__))
#_data = os.path.join(_folder, "jaxon_data")

#def read_script(filepath):
#    try:
#        with open(filepath, "r", encoding="utf-8") as f:
#            return f.read()
#    except Exception:
#        return ""

#loading data to keep it consistent
df = pd.read_csv("data/raw_data.csv")

st.header("Jaxon's Findings")

# Chi-Square ================================================================
st.subheader("Chi-Square Test")
st.write("Association between volunteer/patron roles and how they found the pantry.")

st.subheader("Data")
#replicating what clean.py did originially 
# Target columns to answer the question
rolecol = 'Are you a volunteer or a patron?'
volcol = 'How did you find out about volunteering at the Pantry?'
patroncol = 'How did you first hear about the Pantry?'
# Combine how volunteers and patrons found the pantry
df['how they found the pantry'] = df[volcol].fillna(df[patroncol])
# Created cleaned data
cleaned_df = df[[rolecol, 'how they found the pantry']].copy()
cleaned_df.columns = ['role', 'how they found the pantry']
# Remove rows with no answers
cleaned_df = cleaned_df.dropna(subset=['how they found the pantry'])
# Clean text func
def clean(text):
    text = str(text).strip().lower().title()
    # Mapping outliers to standard categories
    notstandard = {
        'Fairs With The Pantry As A Booth': 'Tabling Event',
        'A Career Discovery Class': 'Campus Resources',
        'Sister': 'Friends',
        'Friends And Used To Be A Volunteer': 'Friends',
        'During Campus Tour': 'Campus Resources',
        'First Year Orientation': 'Campus Resources',
        'I Was A Tour Guide And The Pantry Was A Mandatory Item On The Script': 'Campus Resources',
        'Campus Orientation': 'Campus Resources'
    }
    return notstandard.get(text, text)
# Clean the data
cleaned_df['how they found the pantry'] = cleaned_df['how they found the pantry'].apply(clean)
cleaned_df['role'] = cleaned_df['role'].str.strip().str.title()

#CHANGE = instead of exporting to csv we just make the df here and use
df1 = cleaned_df.copy()
df1.columns = ['Role', 'Discovery_Method']

#df1 = pd.read_csv(os.path.join(_data, "cleanq1data.csv"))
st.dataframe(df1, height=400, use_container_width=True)


#st.subheader("Data Cleaning Script")
#importing script without using os
with st.expander("Show Data Cleaning Script:"):
    st.code(""" 
import pandas as pd
df = pd.read_csv('c1pantryresponsedata.csv')

# Target columns to answer the question
rolecol = 'Are you a volunteer or a patron?'
volcol = 'How did you find out about volunteering at the Pantry?'
patroncol = 'How did you first hear about the Pantry?'

# Combine how volunteers and patrons found the pantry
df['how they found the pantry'] = df[volcol].fillna(df[patroncol])

# Created cleaned data
cleaned_df = df[[rolecol, 'how they found the pantry']].copy()
cleaned_df.columns = ['role', 'how they found the pantry']

# Remove rows with no answers
cleaned_df = cleaned_df.dropna(subset=['how they found the pantry'])

# Clean text func
def clean(text):
    text = str(text).strip().lower().title()
    
    # Mapping outliers to standard categories
    notstandard = {
        'Fairs With The Pantry As A Booth': 'Tabling Event',
        'A Career Discovery Class': 'Campus Resources',
        'Sister': 'Friends',
        'Friends And Used To Be A Volunteer': 'Friends',
        'During Campus Tour': 'Campus Resources',
        'First Year Orientation': 'Campus Resources',
        'I Was A Tour Guide And The Pantry Was A Mandatory Item On The Script': 'Campus Resources',
        'Campus Orientation': 'Campus Resources'
    }
    
    return notstandard.get(text, text)

# Clean the data
cleaned_df['how they found the pantry'] = cleaned_df['how they found the pantry'].apply(clean)
cleaned_df['role'] = cleaned_df['role'].str.strip().str.title()

# Export to CSV
df1 = cleaned_df.copy()
df1.columns = ['Role', 'Discovery_Method'] 
            """)
#st.code(read_script(os.path.join(_data, "clean.py")), language="python")



#st.subheader("Data Analysis Script")
#st.code(read_script(os.path.join(_data, "PantryDiscoveryChi2.py")), language="python")



#mushed together this section so it makes more sense
st.subheader("Data Analysis and Results")
with st.expander("Data Analysis Script:"):
    st.code("""
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

""")
    
#tbl = pd.crosstab(df1.iloc[:, 0], df1.iloc[:, 1])
#rewrote so it still works 
tbl = pd.crosstab(df1['Role'], df1['Discovery_Method'])
st.dataframe(tbl.T, use_container_width=True)

chi2, p, dof, _ = chi2_contingency(tbl)
st.write(f"Chi-Squared: {chi2:.4f}  |  P-value: {p:.4f}  |  Degrees of Freedom: {dof}")

st.subheader("Analysis")
st.write(
    """
- Since the p-value is less than 0.05, there is a strong association between whether someone is a volunteer or patron and how they found out about the Pantry.
"""
)

st.markdown("---")

# Spearman
st.subheader("Spearman Test")
st.write("Correlation between satisfaction with item selection and number of unique items grabbed.")

st.subheader("Data")
#again just rewritten for consistency + replicating what clean.py and cleanclean.py did for spearman
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
#again no exporting just use and keep here
df2 = cleaned_df[['satisfaction_rating', 'items_grabbed_ordinal']].dropna()

#st.subheader("Data Cleaning Script")
#st.code(read_script(os.path.join(_data, "cleanclean.py")), language="python")
with st.expander("Show Data Cleaning Script:"):
    st.code("""
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
df2 = cleaned_df[['satisfaction_rating', 'items_grabbed_ordinal']].dropna()
print("Cleaned")""")

#st.subheader("Data Analysis Script")
#st.code(read_script(os.path.join(_data, "UniqueItemSpearman.py")), language="python")

st.subheader("Data Analysis and Results")
with st.expander("Show Data Analysis Script:"):
    st.code("""
import pandas as pd
from scipy.stats import spearmanr
df = pd.read_csv('cleanq2data.csv')

#run spearman correlation on cleaned data
rho, p_value = spearmanr(df['satisfaction_rating'], df['items_grabbed_ordinal'])

#print results
print(f"Correlation Coefficient: {rho}")
print(f"P-value: {p_value}")
            """)

rho, pval = spearmanr(df2["satisfaction_rating"], df2["items_grabbed_ordinal"])
st.write(f"Correlation (ρ): {rho:.4f}  |  P-value: {pval:.4f}")

st.subheader("Analysis")
st.write(
    """
- Since the p-value is greater than 0.05, there is no statistically significant correlation between satisfaction of item selection and the number of unique items grabbed.
"""
)
