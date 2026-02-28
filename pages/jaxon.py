import os
import streamlit as st
import pandas as pd
from scipy.stats import chi2_contingency, spearmanr

# Folder next to this script
_folder = os.path.dirname(os.path.abspath(__file__))
_data = os.path.join(_folder, "jaxon_data")


def read_script(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


st.header("Jaxon's Findings")

# Chi-Square
st.subheader("Chi-Square Test")
st.write("Association between volunteer/patron role and how they found the pantry.")
st.subheader("Data")
df1 = pd.read_csv(os.path.join(_data, "cleanq1data.csv"))
st.dataframe(df1, height=400, use_container_width=True)
st.subheader("Data Cleaning Script")
st.code(read_script(os.path.join(_data, "clean.py")), language="python")
st.subheader("Data Analysis Script")
st.code(read_script(os.path.join(_data, "PantryDiscoveryChi2.py")), language="python")
st.subheader("Results")
tbl = pd.crosstab(df1.iloc[:, 0], df1.iloc[:, 1])
st.dataframe(tbl.T, use_container_width=True)
chi2, p, dof, _ = chi2_contingency(tbl)
st.write(f"Chi-Squared: {chi2:.4f}  |  P-value: {p:.4f}  |  Degrees of Freedom: {dof}")
st.subheader("Analysis")
st.write("will fill in analysis")

st.markdown("---")

# Spearman
st.subheader("Spearman Test")
st.write("Correlation between satisfaction with item selection and number of unique items grabbed.")
st.subheader("Data")
df2 = pd.read_csv(os.path.join(_data, "cleanq2data.csv"))
st.dataframe(df2, height=400, use_container_width=True)
st.subheader("Data Cleaning Script")
st.code(read_script(os.path.join(_data, "cleanclean.py")), language="python")
st.subheader("Data Analysis Script")
st.code(read_script(os.path.join(_data, "UniqueItemSpearman.py")), language="python")
st.subheader("Results")
rho, pval = spearmanr(df2["satisfaction_rating"], df2["items_grabbed_ordinal"])
st.write(f"Correlation (ρ): {rho:.4f}  |  P-value: {pval:.4f}")
st.subheader("Analysis")
st.write("will fill in analysis")
