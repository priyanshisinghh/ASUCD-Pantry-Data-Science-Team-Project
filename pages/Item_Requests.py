import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
import matplotlib.pyplot as plt
import seaborn as sns
import base64

st.set_page_config(page_title="Item Requests & Produce Availability")

def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("pages/images/pri-bg.png")

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

st.title("Item Requests & Produce Availability")

st.markdown("---")

st.header("The Big Question")
st.write("""
When patrons struggle to find produce at the Pantry, are they more likely to be 
looking for specific types of items such as snacks, fruits, or protein?

If we can identify certain item types that are consistently harder to find, we can identify which items the Pantry should consider prioritizing stocking.
""")

st.markdown("---")

st.header("How We Approached This")
st.write("""
We used a statistical test called a **Chi-Square test**. Here's what that means in plain English:

Imagine splitting all survey respondents into two groups:
- People who said they **want more snacks** at the Pantry
- And the people who said they **don't need more snacks**

Then we ask: do these two groups report finding produce at different rates?

If yes → there's a real pattern worth paying attention to.

If no → it's probably just random variation in the data.

We ran this test separately for three differentitem categories: **Fruits/Vegetables**, **Snacks**, and **Protein (Eggs/Tofu)**.
""")

with st.expander("Show the full list of item categories in the survey"):
    st.write("""
    The survey asked patrons what types of items they'd like to see more of. The options were:
    - Fruits/Vegetables
    - Grains
    - Snacks
    - Non-perishables (Canned goods)
    - Healthcare/Toiletries
    - Meals (DC meals)
    - Eggs/Tofu (Protein)
    """)

st.markdown("---")

# --- Load & clean ---
df = pd.read_csv("data/raw_data.csv")
df_patrons = df[df['Are you a volunteer or a patron?'] == 'Patron'].copy()

availability_col = 'How often do you find the produce you need? '
items_col = 'What types of items would you like to see more of at the Pantry?'
satisfaction_col = 'Rate your satisfaction of the item selection'

df_clean = df_patrons[[availability_col, items_col, satisfaction_col]].dropna().copy()
df_clean.columns = ['availability', 'items_requested', 'satisfaction']
df_clean['satisfaction'] = pd.to_numeric(df_clean['satisfaction'], errors='coerce')
df_clean = df_clean.dropna(subset=['satisfaction'])

CATEGORIES = {
    'Fruits/Vegetables': 'Fruits/Vegetables',
    'Snacks': 'Snacks',
    'Eggs/Tofu (Protein)': 'Eggs/Tofu (Protein)',
    'Grains': 'Grains',
    'Non-perishables (Canned goods)': 'Non-perishables (Canned goods)',
    'Healthcare/Toiletries': 'Healthcare/Toiletries',
    'Meals (DC meals)': 'Meals (DC meals)'
}

for label, keyword in CATEGORIES.items():
    df_clean[label] = df_clean['items_requested'].apply(
        lambda x, k=keyword: 1 if k in str(x) else 0
    )

availability_order = {
    'Never': 1, 'Rarely': 2, 'Sometimes': 3, 'Often': 4, 'Always': 5
}
df_clean['availability_score'] = df_clean['availability'].map(availability_order)

with st.expander("Show Cleaning Script"):
    st.code("""
df = pd.read_csv("data/raw_data.csv")
df_patrons = df[df['Are you a volunteer or a patron?'] == 'Patron'].copy()
df_clean = df_patrons[[availability_col, items_col, satisfaction_col]].dropna().copy()

# Create binary flag for each item category
for label, keyword in CATEGORIES.items():
    df_clean[label] = df_clean['items_requested'].apply(
        lambda x: 1 if keyword in str(x) else 0
    )
    """, language="python")

st.markdown("---")

# --- Key finding upfront ---
st.header("The Key Finding")
st.success("""
Between all the different categories, **snacks** is the only item category where a statistically significant pattern was found.

Patrons who want more snacks report finding produce less often than patrons who don't 
request more snacks, suggesting that these patrons may feel the Pantry's overall selection 
doesn't meet their needs.
""")

st.markdown("---")

# --- Interactive section ---
st.header("Explore by Item Category")
st.write("Select an item category below to see how patrons who want that item report their produce availability.")

selected = st.selectbox("I want to explore patrons looking for:", list(CATEGORIES.keys()))

group = df_clean[df_clean[selected] == 1]
not_group = df_clean[df_clean[selected] == 0]

total_group = len(group)
total_not = len(not_group)

st.markdown("---")

col1, col2 = st.columns(2)
col1.metric(f"Patrons wanting more {selected}", total_group)
col2.metric(f"Patrons not requesting {selected}", total_not)

# Availability breakdown chart
fig, axes = plt.subplots(1, 2, figsize=(10, 4))

for ax, data, label in zip(
    axes,
    [group, not_group],
    [f"Wants more {selected}", f"Doesn't request {selected}"]
):
    counts = data['availability'].value_counts().reindex(
        ['Never', 'Rarely', 'Sometimes', 'Often', 'Always'], fill_value=0
    )
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    counts.plot(kind='bar', ax=ax, color='#8B6914', edgecolor='white')
    ax.set_title(label, fontsize=11)
    ax.set_xlabel("How often they find produce")
    ax.set_ylabel("Number of patrons")
    ax.tick_params(axis='x', rotation=30)
    sns.despine(ax=ax)

plt.tight_layout()
st.pyplot(fig)

# Chi-square result
tbl = pd.crosstab(df_clean[selected], df_clean['availability'])
chi2, p, dof, _ = chi2_contingency(tbl)

st.write(f"**Chi-Squared:** {chi2:.4f} | **P-value:** {p:.4f} | **Degrees of Freedom:** {dof}")

if p < 0.05:
    st.success(f"There IS a statistically significant association between wanting more **{selected}** and produce availability (p < 0.05). This pattern is unlikely to be due to chance.")
else:
    st.info(f"No statistically significant association found for **{selected}** (p ≥ 0.05). The difference between groups is likely due to random variation.")

st.markdown("---")

# --- Full results summary ---
st.header("Full Results Summary")
st.write("Here's how all item categories performed in the chi-square test:")

results = []
for label in CATEGORIES.keys():
    tbl = pd.crosstab(df_clean[label], df_clean['availability'])
    chi2, p, dof, _ = chi2_contingency(tbl)
    results.append({
        'Item Category': label,
        'Chi-Squared': round(chi2, 4),
        'P-value': round(p, 4),
        'Significant?': 'YES!' if p < 0.05 else 'No'
    })

results_df = pd.DataFrame(results)
st.dataframe(results_df, use_container_width=True, hide_index=True)

st.markdown("---")

st.header("What This Means...)
st.write("""
Out of all the item categories tested, **Snacks** stood out as the only one with a 
statistically significant relationship to produce availability. 

This means that patrons who are looking for more snacks tend to also struggle 
more with finding produce, potentially suggesting that this group of patrons finds the 
Pantry's overall selection less aligned with what they're looking for — not just in 
one category, but more broadly.

**Potential Action Items:** The Pantry could consider expanding its snack offerings and 
surveying snack-seeking patrons more directly to understand what specific items would 
make the biggest difference.
""")

st.markdown("---")

st.header("Conclusion")
st.write("""
This analysis tested whether patrons looking for specific item types experience 
produce availability differently. Most categories showed no significant pattern, 
but snack-seekers stood out as a group worth paying more attention to.

Future surveys could ask more specifically about snack preferences and whether 
current snack offerings feel adequate, which would help the Pantry make more 
targeted stocking decisions.
""")
