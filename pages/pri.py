import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.header("Chi-Squared Testing")
st.write(""" Is there an association between "How often patrons find what they need" and "Types of items requested" (fruits, snacks, protein)""")

st.subheader("About the Dataset and Project")
df = pd.read_csv('raw_data.csv')  # CHANGE THIS!

#filter for patrons
df_patrons = df[df['Are you a volunteer or a patron?'] == 'Patron'].copy()
print(f"Patron responses: {len(df_patrons)}")

df_patrons
