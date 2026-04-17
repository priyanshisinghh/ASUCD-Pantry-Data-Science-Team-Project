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

But an important question that we want to analyze is:
**Do all students have the same experience finding the produce they need?**
""")


st.divider()



st.subheader("Research Question")

st.write("""
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

df_clean['ethnicity_label'] = df_clean['ethnicity'].apply(
    lambda x: 'Hispanic' if 'Hispanic' in str(x) else 'Non-Hispanic'
)


st.subheader("Cleaned Dataset")
st.dataframe(df_clean[['race','ethnicity','produce_availability','rare_never']])

# user selection
st.markdown("---")
st.subheader("Interactive Analysis")

analysis_type = st.selectbox(
    "Choose a demographic grouping:",
    ["Race", "Asian vs. Non-Asian", "Ethnicity (Hispanic vs. Non-Hispanic)"]
)

# determining group
if analysis_type == "Race":
    group_col = 'race'
elif analysis_type == "Asian vs Non-Asian":
    group_col = 'asian_label'
else:
    group_col = 'ethnicity_label'

df_analysis = df_clean[df_clean[group_col].notna()].copy()



# CONTINGENCY TABLE
table = pd.crosstab(df_analysis[group_col], df_analysis['rare_never'])
table.columns = ['Sometimes/Always', 'Rarely/Never']

chi2, p, dof, expected = chi2_contingency(table)

st.write("### Contingency Table")
st.dataframe(table)

# RESULTS
st.write(f"Chi-Square: {chi2:.4f}")
st.write(f"P-value: {p:.4f}")
st.write(f"Degrees of Freedom: {dof}")

#interpretation by selection
st.subheader("What This Means")

if analysis_type == "Race":
    st.write("""
This test compares multiple race categories to see whether some groups report
difficulty finding produce more often than others.

Because there are many race categories, some groups may have very small sample sizes,
which can make the chi-square result less reliable.
""")
    # significance result
    if p < 0.05:
        st.error("""
    The p-value is less than 0.05, which means there is a statistically significant relationship
    between the selected demographic group and difficulty finding produce.
    """)
    else:
        st.success("""
    The p-value is greater than 0.05, meaning there is no statistically significant relationship
    between the selected demographic group and difficulty finding produce.
    """)

elif analysis_type == "Asian vs. Non-Asian":
    st.write("""
This test simplifies the data into two groups: Asian and Non-Asian.

This helps ensure that group sizes are large enough for a more reliable comparison
and makes the statistical test more valid.
""")
        # significance result
    if p < 0.05:
        st.error("""
    The p-value is less than 0.05, which means there is a statistically significant relationship
    between the selected demographic group and difficulty finding produce.
    """)
    else:
        st.success("""
    The p-value is greater than 0.05, meaning there is no statistically significant relationship
    between the selected demographic group and difficulty finding produce.
    """)

else:
    st.write("""
This test compares Hispanic vs. Non-Hispanic students to examine whether ethnicity
is associated with difficulty finding produce.

This grouping also improves statistical validity by ensuring sufficient sample sizes.
""")
    # significance result
    if p < 0.05:
        st.error("""
    The p-value is less than 0.05, which means there is a statistically significant relationship
    between the selected demographic group and difficulty finding produce.
    """)
    else:
        st.success("""
    The p-value is greater than 0.05, meaning there is no statistically significant relationship
    between the selected demographic group and difficulty finding produce.
    """)


# VISUALIZATION
st.subheader("Visualization")
st.bar_chart(table)


# INTERPRETATION (DYNAMIC)
st.subheader("Interpretation")

if p < 0.05:
    st.error("""
There is a statistically significant relationship between the selected demographic group
and difficulty finding produce.
""")
else:
    st.success("""
No statistically significant relationship was detected between the selected demographic group
and difficulty finding produce.
""")

st.write("""
This does not necessarily mean disparities do not exist.  
This analysis focuses on general produce availability and may not capture culturally specific food needs.

Future surveys could better address this by asking directly about culturally relevant foods.
""")



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
