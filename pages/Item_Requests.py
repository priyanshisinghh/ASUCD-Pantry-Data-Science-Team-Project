import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency

#page background
import base64

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
#end background content

st.header("Pri's Findings")

st.write("""
### Research Question
Is there an association between **how often patrons find the produce they need** and 
**what types of items they want more of** (fruits, snacks, protein)?
""")

st.markdown("---")

# --- Load & clean inline ---
df = pd.read_csv("data/raw_data.csv")

df_patrons = df[df['Are you a volunteer or a patron?'] == 'Patron'].copy()

availability_col = 'How often do you find the produce you need? '
items_col = 'What types of items would you like to see more of at the Pantry?'

df_clean = df_patrons[[availability_col, items_col]].dropna().copy()
df_clean.columns = ['availability', 'items_requested']

# Binary flags for each item type
df_clean['wants_fruit']   = df_clean['items_requested'].apply(lambda x: 1 if 'fruit' in str(x).lower() else 0)
df_clean['wants_snacks']  = df_clean['items_requested'].apply(lambda x: 1 if 'snack' in str(x).lower() else 0)
df_clean['wants_protein'] = df_clean['items_requested'].apply(lambda x: 1 if 'protein' in str(x).lower() else 0)

st.subheader("Cleaned Dataset")
st.dataframe(df_clean)

with st.expander("Show Cleaning Script"):
    st.code("""
df = pd.read_csv("data/raw_data.csv")
df_patrons = df[df['Are you a volunteer or a patron?'] == 'Patron'].copy()

availability_col = 'How often do you find the produce you need? '
items_col = 'What types of items would you like to see more of at the Pantry?'

df_clean = df_patrons[[availability_col, items_col]].dropna().copy()
df_clean.columns = ['availability', 'items_requested']

df_clean['wants_fruit']   = df_clean['items_requested'].apply(lambda x: 1 if 'fruit' in str(x).lower() else 0)
df_clean['wants_snacks']  = df_clean['items_requested'].apply(lambda x: 1 if 'snack' in str(x).lower() else 0)
df_clean['wants_protein'] = df_clean['items_requested'].apply(lambda x: 1 if 'protein' in str(x).lower() else 0)
    """, language="python")

st.markdown("---")

# --- Chi-Square for each item type ---
for item_label, item_col in [('Fruits', 'wants_fruit'), ('Snacks', 'wants_snacks'), ('Protein', 'wants_protein')]:
    st.subheader(f"Chi-Square: Produce Availability vs. Wanting More {item_label}")

    tbl = pd.crosstab(df_clean['availability'], df_clean[item_col])
    tbl.columns = [f'Does not request {item_label}', f'Requests {item_label}']
    st.dataframe(tbl)

    chi2, p, dof, _ = chi2_contingency(tbl)
    st.write(f"Chi-Squared: {chi2:.4f} | P-value: {p:.4f} | Degrees of Freedom: {dof}")

    if p < 0.05:
        st.write(f"✅ Significant association between produce availability and wanting more {item_label} (p < 0.05).")
    else:
        st.write(f"No statistically significant association between produce availability and wanting more {item_label} (p ≥ 0.05).")

    st.markdown("---")

st.subheader("Conclusion")
st.write("""
This analysis tested whether patrons who struggle to find produce are more likely to 
request specific item types (fruits, snacks, or protein).

Results above show whether unmet produce needs are tied to specific item preferences,
which could help the Pantry prioritize what to stock.
""")
