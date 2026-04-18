import streamlit as st
import pandas as pd
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import base64

# MUST BE FIRST
st.set_page_config(page_title="Andrew's Findings", layout="centered")

# background
def get_base64(file_path):
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

img = get_base64("pages/images/andrew-bg.png")

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
    section.main > div {{
        background-color: rgba(255, 255, 255, 0.95);
        padding: 30px;
        border-radius: 16px;
        max-width: 1100px;
        margin: auto;
    }}
    details summary {{
        color: black !important;
        background-color: white !important;
    }}
    details[open] > summary {{
        background-color: white !important;
    }}
    details {{
        background-color: white !important;
    }}
    </style>
""", unsafe_allow_html=True)

# rest of your code unchanged...

#loading and cleaning data
@st.cache_data
def load_data():
    return pd.read_csv("data/raw_data.csv")

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

#making models
m1 = smf.ols('Experience ~ Satisfaction', data=modeldata).fit()
m2 = smf.ols('Experience ~ Satisfaction + C(Gender)', data=modeldata).fit()
m3 = smf.ols('Experience ~ Satisfaction + C(Gender) + C(College)', data=modeldata).fit()

#layout of streamlit

st.title("How Shopping Experience is Impacted by Satisfaction, Gender, and Major")
st.write("*Our analysis of the ASUCD Pantry Patron Data*")
st.divider()

#main idea
st.header("Main Finding")
st.success("**Satisfaction with the items provided is the only significant factor in determining a patron's overall shopping experience.**")

st.markdown("""
When we look at the data, we can see the demographics of our patrons, what they study and how they identify their own gender. This doesn't negatively or positively impact how welcoming they find The Pantry. 

The Pantry's environment is consistently welcoming across different student populations, which is a great thing! If we want to elevate the overall shopping experience, our main focus should be to improve the items we stock.
""")

st.divider()

#prediction tool 
st.header("Test your own experience with our model!")
st.write("We built a predictive machine learning model based on the survey data. You can change the metrics below to see how they impact the predicted overall shopping experience.")

with st.form("prediction_form"):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        #using a slider for satisfaction 
        user_sat = st.slider("Item Satisfaction Level", 1.0, 5.0, 3.0, 0.5)
    with col2:
        user_gender = st.selectbox("Patron Gender", modeldata['Gender'].unique())
    with col3:
        user_college = st.selectbox("Patron College", modeldata['College'].unique())
        
    submitted = st.form_submit_button("Predict the Overall Shopping Experience!")

if submitted:
    #creates a dataframe with whatever the person inputs
    input_df = pd.DataFrame({
        'Satisfaction': [user_sat],
        'Gender': [user_gender],
        'College': [user_college]
    })
    
    #predicts using m3 (which was the most complex model)
    prediction = m3.predict(input_df).iloc[0]
    
    #stops the prediction from going over 5, since that is the max score
    prediction = min(prediction, 5.0)
    
    st.info(f"### Predicted Overall Experience: **{prediction:.2f} / 5.00**")

st.divider()

#visuals
st.header("The Visual Proof")

col_text, col_plot = st.columns([1, 2])

with col_text:
    st.write("### Effect of Item Satisfaction")
    st.write("""
    Each blue dot represents a student's survey response. Because many people gave the same score, the dots are slightly spread out so we can see the density. 
    
    The **red line** represents our predictive model: as item satisfaction goes up, the overall experience clearly trends up with it.
    """)

with col_plot:
    fig, ax = plt.subplots(figsize=(6, 4))
    #made background transparent 
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.tick_params(colors='black')
    ax.xaxis.label.set_color('black')
    ax.yaxis.label.set_color('black')
    
    sns.regplot(
        data=modeldata, 
        x='Satisfaction', 
        y='Experience', 
        scatter_kws={'alpha': 0.6, 'color': '#1f77b4'}, 
        line_kws={'color': '#ff7f0e'},
        x_jitter=0.2, 
        y_jitter=0.2,
        ax=ax
    )
    ax.set_xlabel("Satisfaction with Items (1-5)")
    ax.set_ylabel("Overall Shopping Experience (1-5)")
    sns.despine()
    st.pyplot(fig)

st.divider()

#model comparison and anova testing 
st.header("The Model Comparisons and ANOVA Tests"):
st.markdown("""
Our base model explains about **27.5%** of the variance in the shopping experience. Notice that when we add Gender and College to the model, the Adjusted R-Squared actually *drops*. This mathematically proves that those demographic variables are just adding noise, not predictive value.
    
*The base regression equation:* y = 2.60 + 0.45x""")
    
#showing the data
met_col1, met_col2, met_col3 = st.columns(3)
met_col1.metric("Model 1 (Satisfaction Only)", f"{m1.rsquared_adj:.3f}", "Baseline Adj. R²")
met_col2.metric("Model 2 (+ Gender)", f"{m2.rsquared_adj:.3f}", f"{(m2.rsquared_adj - m1.rsquared_adj):.3f}", delta_color="inverse")
met_col3.metric("Model 3 (+ College)", f"{m3.rsquared_adj:.3f}", f"{(m3.rsquared_adj - m1.rsquared_adj):.3f}", delta_color="inverse")
    
st.write("---")
st.write("### Exploring Demographics")
st.write("Even though gender and college don't drive the overall experience, it is still helpful to see who is using the space. Our data shows more female respondents than male, heavily concentrated in the CAES and L&S colleges.")
    
#faceted grid plot
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
    scatter_kws={'alpha': 0.6},
    height=3,
    aspect=1.2
    )
    
#making the faceted grid transparent
g.fig.patch.set_facecolor('white')
for ax in g.axes.flatten():
    ax.set_facecolor('white')
    ax.tick_params(colors='black')
        
g.fig.subplots_adjust(top=0.9)
g.fig.suptitle("Panels: College | Color: Gender | X-axis: Satisfaction")
st.pyplot(g.fig)
