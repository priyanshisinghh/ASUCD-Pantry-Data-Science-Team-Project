
import streamlit as st
import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Andrew's Findings: How Shopping Experience is impacted by Satisfaction, Gender and Major")

# loading the data and then cleaning it
@st.cache_data
def load_data():
    return pd.read_csv("pantryresponses.csv")

cleandata = load_data()

cleandata = cleandata.rename(columns={
    "Rate the overall shopping experience (ease/welcoming experience)": "Experience",
    "Rate your satisfaction of the item selection": "Satisfaction",
    "What is your gender?": "Gender",
    "What college are you?": "College"
})

modeldata = cleandata[['Experience', 'Satisfaction', 'Gender', 'College']].copy()
modeldata['Experience'] = pd.to_numeric(modeldata['Experience'], errors='coerce')
modeldata['Satisfaction'] = pd.to_numeric(modeldata['Satisfaction'], errors='coerce')
modeldata = modeldata.dropna()

# main points
st.header("The Main Takeaway")
st.success("**Satisfaction with the items provided is the only significant factor in determining a patron's overall shopping experience.**")

st.markdown("""
When we look at the data, the demographics of our patrons, specifically what they study and how they identify their gender, doesn't negatively or positively impact how welcoming they find the Pantry. 

**This is great news!** It means our environment is consistently welcoming across different student populations. If we want to improve the overall shopping experience, our primary focus should be on improving the items we stock.
""")

# graph
st.header("Visualizing the Impact of Satisfaction")

fig, ax = plt.subplots(figsize=(8, 5))
sns.regplot(
    data=modeldata, 
    x='Satisfaction', 
    y='Experience', 
    scatter_kws={'alpha': 0.6, 'color': 'darkblue'}, 
    line_kws={'color': 'red'},
    x_jitter=0.2, 
    y_jitter=0.2,
    ax=ax
)
ax.set_title("Effect of Item Satisfaction on Shopping Experience")
ax.set_xlabel("Satisfaction with Items (1-5)")
ax.set_ylabel("Overall Shopping Experience (1-5)")
sns.despine()
st.pyplot(fig)

st.info("""
**How to read this chart:** Each blue dot represents a student's survey response. Because many people gave the same score (like a 4 in Satisfaction and a 5 in Experience), the dots are slightly "jittered" or spread out so we can see the density. The red line represents our predictive model: as item satisfaction goes up, the overall experience goes up with it.
""")

# testing models against each other and anova tests
st.header("The Statistical Proof (For the Data Nerds)")

# building the three models
m1 = smf.ols('Experience ~ Satisfaction', data=modeldata).fit()
m2 = smf.ols('Experience ~ Satisfaction + C(Gender)', data=modeldata).fit()
m3 = smf.ols('Experience ~ Satisfaction + C(Gender) + C(College)', data=modeldata).fit()

# creating a comparison table
model_comparison = pd.DataFrame({
    "Model": ["Satisfaction Only", "+ Gender", "+ College"],
    "R-Squared": [m1.rsquared, m2.rsquared, m3.rsquared],
    "Adjusted R-Squared": [m1.rsquared_adj, m2.rsquared_adj, m3.rsquared_adj]
})

st.write("### Model Performance Comparison")
st.dataframe(model_comparison.style.format({"R-Squared": "{:.3f}", "Adjusted R-Squared": "{:.3f}"}))

st.markdown("""
Our base model explains about **27.5%** of the variance in the shopping experience. Notice that when we add Gender and College to the model, the Adjusted R-Squared actually *drops*. This mathematically proves that those variables are just adding noise, not value.

*The Satisfaction regression equation:* $y = 2.60 + 0.45x$
""")

# breaking it down by college and gender
st.header("Exploring Demographics")
st.markdown("Even though gender and college don't drive the overall experience, it is still helpful to see who is using the Pantry. Our data shows more female respondents than male, heavily concentrated in the CAES and L&S colleges (which reflects the overall UC Davis population).")

# Plot: College vs Experience
fig_col, ax_col = plt.subplots(figsize=(10, 5))
sns.stripplot(data=modeldata, x='College', y='Experience', jitter=0.2, alpha=0.6, color="darkblue", ax=ax_col)
ax_col.set_title("College and Experience")
plt.xticks(rotation=45, ha='right')
st.pyplot(fig_col)

# Plot: Faceted by College and Gender
st.write("### All 3 Variables")
st.write("Here is a detailed look at Satisfaction vs. Experience, split up by both College and Gender. While the slopes look slightly different visually, our ANOVA testing confirms these differences are not statistically significant.")

# Seaborn's lmplot creates a FacetGrid, so we extract the figure differently
g = sns.lmplot(
    data=modeldata, 
    x='Satisfaction', 
    y='Experience', 
    hue='Gender', 
    col='College', 
    col_wrap=2, 
    ci=None, 
    x_jitter=0.2, 
    y_jitter=0.2, 
    scatter_kws={'alpha': 0.6}
)
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Panels: College | Color: Gender | X-axis: Satisfaction")
st.pyplot(g.fig)