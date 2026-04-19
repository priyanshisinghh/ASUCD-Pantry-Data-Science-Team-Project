import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency, spearmanr
import base64

st.set_page_config(page_title="ASUCD Pantry Outreach and Inventory Satisfaction Analysis")

#background stuff
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("pages/images/jaxon-bg.png")

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
#background stuff end

@st.cache_data
def load_data():
    return pd.read_csv("data/raw_data.csv")

df = load_data()

st.title("ASUCD Pantry Outreach and Inventory Satisfaction Analysis")
st.write("*The effectiveness of outreach methods and the influence of inventory on patron satisfaction*")

st.markdown("""
Outreach is very important to the Pantry's mission, so analyzing the effectiveness of our outreach methods is crucial to improving
recruitment and understanding how to reach more patrons.
We used a Chi-Square test to analyze the relationship between volunteer/patron roles and how they discovered the Pantry.
Another question we found important to answer is how to improve patron satisfaction via the item selection.
We also used a Spearman test to analyze the relationship between satisfaction with the item selection and the number of unique items grabbed.
""")

st.divider()

# Summary metrics
total = len(df)
volunteers = (df['Are you a volunteer or a patron?'].str.strip().str.title() == 'Volunteer').sum()
patrons = (df['Are you a volunteer or a patron?'].str.strip().str.title() == 'Patron').sum()

m1, m2, m3 = st.columns(3)
m1.metric("Total Responses", total)
m2.metric("Volunteers", int(volunteers))
m3.metric("Patrons", int(patrons))

st.divider()

# Chi-Square intro
st.header("Chi-Square Test")

st.markdown("""
**Research question:** Is there a statistically significant relationship between a person's role (volunteer vs. patron) and how they first discovered the Pantry?

If volunteers and patrons discover the Pantry through meaningfully different methods, the Pantry could tailor its outreach strategy to each audience more effectively. In addition, understanding which methods are more or less effective in general will help the Pantry focus its outreach efforts more effectively.

We used a Chi-Square test of independence because both variables are categorical: role (volunteer or patron) and discovery method (social media, friends, etc.). The Chi-Square test tells us whether the discovery methods differs significantly between the two groups, or whether any difference between the two is due to chance.
""")

st.divider()

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

with st.expander("Show Raw Data"):
    st.dataframe(df1, height=300, use_container_width=True)


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



st.subheader("Filter by Role")
role_filter = st.selectbox("Filter by role:", ["All", "Volunteer", "Patron"])

if role_filter == "All":
    df1_filtered = df1
else:
    df1_filtered = df1[df1['Role'] == role_filter]

# Bar chart of discovery methods
st.subheader("Discovery Methods")
col_chart, col_info = st.columns([2, 1])

with col_chart:
    method_counts = df1_filtered['Discovery_Method'].value_counts()
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    method_counts.plot(kind='bar', ax=ax, color='#8B6914', edgecolor='white')
    ax.set_xlabel("Discovery Method")
    ax.set_ylabel("Count")
    ax.set_title(f"How {'Everyone' if role_filter == 'All' else role_filter + 's'} Found the Pantry")
    plt.xticks(rotation=35, ha='right')
    plt.tight_layout()
    sns.despine()
    st.pyplot(fig)

with col_info:
    st.write("**Top discovery method:**")
    st.info(f"**{method_counts.index[0]}** ({method_counts.iloc[0]} responses)")
    st.write("**Total responses shown:**")
    st.metric("", len(df1_filtered))

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

tbl = pd.crosstab(df1['Role'], df1['Discovery_Method'])
with st.expander("Show Contingency Table"):
    st.dataframe(tbl.T, use_container_width=True)

chi2, p, dof, _ = chi2_contingency(tbl)
c1, c2, c3 = st.columns(3)
c1.metric("Chi-Squared", f"{chi2:.4f}")
c2.metric("P-value", f"{p:.4f}")
c3.metric("Degrees of Freedom", dof)

st.subheader("Analysis")
if p < 0.05:
    st.info("Since the p-value is less than 0.05, there is a strong association between whether someone is a volunteer or patron and how they found out about the Pantry.")
else:
    st.info("The p-value is greater than 0.05 — no statistically significant association detected.")

st.markdown("""
The Chi-Square test reveals that volunteers and patrons do not generally find the Pantry the same way.

For the Pantry, this means that outreach should be approached differently for each group. Patron outreach should lean into things that work like campus resource fairs. Volunteer recruitment may benefit more from targeted efforts like class announcements or formal campus involvement programs.
""")

st.divider()

# Spearman
st.header("Spearman Test")

st.markdown("""
**Research question:** Is there a correlation between how satisfied a patron is with the item selection and how many unique items they grab during a visit?

We used a Spearman rank correlation because the "items grabbed" variable is ordinal (respondents chose from ranges like "1-2 items", "3-5 items", etc.) rather than a precise count. Spearman is designed for ranked data and doesn't assume a linear relationship between the two variables.
""")

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

with st.expander("Show Raw Data"):
    st.dataframe(df2, height=300, use_container_width=True)

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

#big change

sp1, sp2 = st.columns(2)
sp1.metric("Correlation (ρ)", f"{rho:.4f}")
sp2.metric("P-value", f"{pval:.4f}")

st.subheader("Visualize the Relationship")

sat_filter = st.slider(
    "Filter by minimum satisfaction rating:",
    min_value=int(df2['satisfaction_rating'].min()),
    max_value=int(df2['satisfaction_rating'].max()),
    value=int(df2['satisfaction_rating'].min())
)

df2_filtered = df2[df2['satisfaction_rating'] >= sat_filter]

item_label_map = {1: '1-2 items', 2: '3-5 items', 3: '6-10 items', 4: '10+ items'}
df2_plot = df2_filtered.copy()
df2_plot['items_label'] = df2_plot['items_grabbed_ordinal'].map(item_label_map)

col_scatter, col_bar = st.columns(2)

with col_scatter:
    fig2, ax2 = plt.subplots(figsize=(5, 4))
    fig2.patch.set_facecolor('white')
    ax2.set_facecolor('white')
    sns.stripplot(
        data=df2_plot,
        x='satisfaction_rating',
        y='items_grabbed_ordinal',
        jitter=0.2,
        alpha=0.5,
        color='#8B6914',
        ax=ax2
    )
    ax2.set_xlabel("Satisfaction Rating (1-5)")
    ax2.set_ylabel("Items Grabbed (ordinal)")
    ax2.set_yticks([1, 2, 3, 4])
    ax2.set_yticklabels(['1-2', '3-5', '6-10', '10+'])
    ax2.set_title("Satisfaction vs. Items Grabbed")
    sns.despine()
    st.pyplot(fig2)

with col_bar:
    fig3, ax3 = plt.subplots(figsize=(5, 4))
    fig3.patch.set_facecolor('white')
    ax3.set_facecolor('white')
    avg_items = df2_plot.groupby('satisfaction_rating')['items_grabbed_ordinal'].mean()
    avg_items.plot(kind='bar', ax=ax3, color='#c4a882', edgecolor='white')
    ax3.set_xlabel("Satisfaction Rating")
    ax3.set_ylabel("Avg. Items Grabbed (ordinal)")
    ax3.set_title("Avg. Items Grabbed by Satisfaction")
    plt.xticks(rotation=0)
    sns.despine()
    st.pyplot(fig3)

st.subheader("Analysis")
if pval < 0.05:
    st.info(f"The p-value is less than 0.05 — there **is** a statistically significant correlation (ρ = {rho:.4f}) between satisfaction and items grabbed.")
else:
    st.info(f"Since the p-value ({pval:.4f}) is greater than 0.05, there is **no statistically significant correlation** between satisfaction of item selection and the number of unique items grabbed.")

st.markdown("""
Satisfaction with the item selection does not predict how many unique items a patron grabs. Patrons tend to grab a similar number of items regardless of how satisfied they are with what's available.

This suggests that the number of items a patron takes is likely driven by other factors (possibly personal need), rather than by how much they like the selection. While improving item quality and variety is still important for overall experience, the Pantry should not expect it alone to increase the volume of food patrons take home.
""")

st.divider()

st.header("What This Means...")
st.write("""
Together, these two findings give the Pantry a clearer picture of where to focus:

**For outreach,** volunteers and patrons are different audiences who find the Pantry 
through different channels. We found that broad campaigns are less effective than targeted ones,
thus suggesting that patron outreach should lean into campus resource fairs and word of mouth. 
Volunteer recruitment benefits more from class announcements and campus involvement programs compared
to other methods of outreach.

**For inventory,** since satisfaction with items doesn't predict how much patrons take home, 
simply stocking more items won't automatically increase food distribution. The focus should 
be on stocking items patrons actually want. This can be found on the item request page. 
""")

st.header("Conclusion")
st.markdown("""
Both findings provide a better idea of what contributes to the Pantry's success.

For outreach, the data confirms that volunteers and patrons are different audiences who discover the Pantry through different means. Targeted, strategies will be more effective than broad campaigns.

For inventory, satisfaction with items does not drive how much patrons take home, meaning that stocking better items alone to increase food distribution.
""")
