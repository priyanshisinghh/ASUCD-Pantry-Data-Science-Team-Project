#import os - removed since we are not using os
import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency

st.markdown("""
<style>
body {
    background-color: #f7f9fc;
}
h1, h2, h3 {
    color: #2c3e50;
}
</style>
""", unsafe_allow_html=True)

# title
st.title("Is There a Relationship Between Student Demographics and the Frequency of Finding Fresh Produce at The Pantry?")
st.write("""
Access to fresh food is essential for student health and well-being.  
At The Pantry, students rely on available produce to meet their nutritional needs.

But an important question that we want to analyze:

**Do all students have the same experience finding the produce they need?**
""")


st.divider()



st.subheader("Research Question")

st.write("""
### Research Question
Is there a significant relationship between student race/ethnicity and the likelihood that they report
they **rarely or never find the produce they need** at the Pantry?
""")

st.markdown("---")

#clean data
df = pd.read_csv("data/raw_data.csv")

df_patrons = df[df['Are you a volunteer or a patron?'] == 'Patron'].copy()

df_patrons = df_patrons.rename(columns={
    'What is your ethnicity?': 'ethnicity',
    'What is your race? [Choose all that apply]': 'race',
    'How often do you find the produce you need? ': 'produce_availability'
})

df_clean = df_patrons.dropna(subset=['produce_availability']).copy()

df_clean['rare_never'] = df_clean['produce_availability'].apply(
    lambda x: 1 if str(x).strip() in ['Rarely', 'Never'] else 0
)

df_clean['asian'] = df_clean['race'].apply(
    lambda x: 1 if 'Asian' in str(x) else 0
)

df_clean['asian_label'] = df_clean['asian'].map({
    1: 'Asian',
    0: 'Non-Asian'
})

st.subheader("Cleaned Dataset")
st.dataframe(df_clean[['race','ethnicity','produce_availability','rare_never']])

# user selection
st.markdown("---")
st.subheader("Interactive Analysis")

analysis_type = st.selectbox(
    "Choose a demographic grouping:",
    ["Race", "Asian vs. Non-Asian", "Ethnicity (Hispanic vs. Non-Hispanic)"]
)

# filters (sidebar)
st.sidebar.header("Filters")

selected_responses = st.sidebar.multiselect(
    "Filter Produce Availability:",
    df_clean['produce_availability'].unique(),
    default=df_clean['produce_availability'].unique()
)

df_filtered = df_clean[df_clean['produce_availability'].isin(selected_responses)]

# determining group
if analysis_type == "Race":
    group_col = 'race'
elif analysis_type == "Asian vs Non-Asian":
    group_col = 'asian_label'
else:
    group_col = 'ethnicity_label'

df_analysis = df_filtered[df_filtered[group_col].notna()].copy()



#added this here so the code is expandable if you want - making more user friendly
with st.expander("Cleaning Script"):
    st.code("""
    df = pd.read_csv("data/raw_data.csv")
df_patrons = df[df['Are you a volunteer or a patron?'] == 'Patron'].copy()
df_patrons = df_patrons.rename(columns={
    'What is your ethnicity?': 'ethnicity',
    'What is your race? [Choose all that apply]': 'race',
    'How often do you find the produce you need? ': 'produce_availability'
})
df_clean = df_patrons.dropna(subset=['produce_availability']).copy()
df_clean['rare_never'] = df_clean['produce_availability'].apply(
    lambda x: 1 if str(x).strip() in ['Rarely', 'Never'] else 0
)
df_clean['asian'] = df_clean['race'].apply(lambda x: 1 if 'Asian' in str(x) else 0)
df_clean['asian_label'] = df_clean['asian'].map({1: 'Asian', 0: 'Non-Asian'})
    """, language="python")





#race analysis
st.subheader("Race-Based Analysis")

st.write("""
Examining whether race is associated with reporting limited produce availability.
""")

race_table = pd.crosstab(df_clean['race'], df_clean['rare_never'])
race_table.columns = ['Sometimes/Always', 'Rarely/Never']

chi2_race, p_race, dof_race, expected_race = chi2_contingency(race_table)

st.write("Contingency Table")
st.dataframe(race_table)

st.write(f"Chi-Square: {chi2_race:.4f}")
st.write(f"P-value: {p_race:.4f}")
st.write(f"Degrees of Freedom: {dof_race}")

expected_race_df = pd.DataFrame(expected_race,
                                index=race_table.index,
                                columns=race_table.columns)

st.subheader("Expected Counts")
st.dataframe(expected_race_df)

st.write("""
Although this test addresses the research question directly,
several expected cell counts are small due to many race categories.

This violates chi-square assumptions, making this result less reliable.
""")

st.markdown("---")

#asian vs nonasian
st.subheader("2: Asian vs Non-Asian")

st.write("""
To improve statistical validity, I grouped respondents into Asian vs. Non-Asian to test groups that are bigger in the data.
""")

asian_table = pd.crosstab(df_clean['asian_label'], df_clean['rare_never'])
asian_table.columns = ['Sometimes/Always', 'Rarely/Never']

chi2_asian, p_asian, dof_asian, expected_asian = chi2_contingency(asian_table)

st.write("Contingency Table")
st.dataframe(asian_table)

st.write(f"Chi-Square: {chi2_asian:.4f}")
st.write(f"P-value: {p_asian:.4f}")
st.write(f"Degrees of Freedom: {dof_asian}")

st.write("""
This grouping satisfied expected count assumptions because they were all greater than 5.
The result showed **no statistically significant relationship** between Asian identity
and reporting difficulty finding produce.
""")

st.markdown("---")

#ethnicity
st.subheader("3: Ethnicity Analysis")

df_eth = df_clean[df_clean['ethnicity'].notna()].copy()

eth_table = pd.crosstab(df_eth['ethnicity'], df_eth['rare_never'])
eth_table.columns = ['Sometimes/Always', 'Rarely/Never']

chi2_eth, p_eth, dof_eth, expected_eth = chi2_contingency(eth_table)

st.write("Contingency Table")
st.dataframe(eth_table)

st.write(f"Chi-Square: {chi2_eth:.4f}")
st.write(f"P-value: {p_eth:.4f}")
st.write(f"Degrees of Freedom: {dof_eth}")

st.write("""
Ethnicity also showed **no statistically significant relationship**
with reporting limited produce availability.
""")

st.markdown("---")

#conclude
st.subheader("Conclusion")

st.write("""
Across race, aggregated race (Asian vs. Non-Asian), and ethnicity analyses, 
no statistically significant relationship was detected between demographic 
identity and reporting that produce was rarely or never available at The Pantry.

This does **not** imply that there are no disparities in access to culturally relevant foods
or that all patrons’ needs are equally met. Our survey primarily asked about general produce availability
and was **not specifically designed to measure cultural food gaps**. 

Future data collection efforts could expand on these findings by incorporating questions that directly address culturally 
specific food availability, enabling a more comprehensive evaluation of whether the pantry is 
meeting the diverse dietary and cultural needs of its patrons.

""")
