import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency
import base64

st.set_page_config(page_title="Risitha's Findings")

#background stuff
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("pages/images/risitha-bg.png")

st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{img}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
    }}
    </style>
""", unsafe_allow_html=True)
#background end

# title
st.title("Student Demographics and the Frequency of Finding Produce at The Pantry")
st.write("""
Access to fresh food is essential for student health and well-being. At The Pantry, students rely on available produce to meet their nutritional needs.

At UC Davis, the undergraduate population is highly diverse, with approximately 35.8% identifying as Asian American and 27.3% as Hispanic/Latino. 
These demographics highlight the importance of ensuring that food resources are accessible and meet the needs of all student groups.

Given this context, an important question that we want to analyze is:

**Do all students have the same experience finding the produce they need?**
""")


st.divider()



st.subheader("Research Question")

st.write("""
Is there a significant relationship between student race/ethnicity and the likelihood that they report
they **rarely or never find the produce they need** at the Pantry?
""")

st.markdown("---")

# clean data
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
st.write("""
### What is this dataset?

To better understand student experiences at The Pantry, we conducted a survey asking students about their demographics and how often they are able to find the produce they need.

The original dataset contains these raw survey responses.  
Before analyzing it, we “clean” the data to make it easier to work with and ensure accurate results.

The table below shows the cleaned version of the data that is used for analysis.
""")
st.dataframe(df_clean[['race','ethnicity','produce_availability','rare_never']])

with st.expander("How was the data cleaned?"):
    st.write("""
This section shows the actual code used to prepare the data for analysis.
This makes the data easier to analyze and allow us to run statistical tests like the chi-square test.

""")
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

#st.code(read_script(os.path.join(_data, "clean_script.py")), language="python")





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
st.caption("Counts represent number of students in each category.")

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
    between Race and difficulty finding produce.
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
    between the Asian vs. Non-Asian group and difficulty finding produce.
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
    between Ethnicity and difficulty finding produce.
    """)


# VISUALIZATION
st.subheader("Visualization")
st.bar_chart(table)


# INTERPRETATION (DYNAMIC)
st.subheader("Interpretation")

if p < 0.05:
    st.error("""
Based on the visualization and p-value result being < 0.5, 
there exists a significant relationship between the selected group and difficulty finding produce.
""")
else:
    st.success("""
Based on the visualization and p-value result being > 0.5, 
there is no significant relationship between the selected group and difficulty finding produce.

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

st.markdown("---")
st.caption("ASUCD Pantry Data Science Team · UC Davis · 2025-2026")
