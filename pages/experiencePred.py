import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

st.header("Combined Model: Predicting a Good Pantry Experience")

st.write("""
This model combines findings from all team members to answer one question:

**Can we predict whether a patron will have a good overall shopping experience 
based on their satisfaction, what they find at the pantry, and their demographics?**
""")

st.markdown("---")

# --- Load & clean ---
df = pd.read_csv("data/raw_data.csv")
df_patrons = df[df['Are you a volunteer or a patron?'] == 'Patron'].copy()

experience_col   = 'Rate the overall shopping experience (ease/welcoming experience)'
satisfaction_col = 'Rate your satisfaction of the item selection'
availability_col = 'How often do you find the produce you need? '
gender_col       = 'What is your gender?'
college_col      = 'What college are you?'
year_col         = 'What year are you?'

df_model = df_patrons[[
    experience_col, satisfaction_col, availability_col,
    gender_col, college_col, year_col
]].copy()

df_model.columns = [
    'experience', 'satisfaction', 'availability',
    'gender', 'college', 'year'
]

df_model['experience']   = pd.to_numeric(df_model['experience'], errors='coerce')
df_model['satisfaction'] = pd.to_numeric(df_model['satisfaction'], errors='coerce')
df_model = df_model.dropna()

# Target: good experience = 4 or 5
df_model['good_experience'] = (df_model['experience'] >= 4).astype(int)

# Encode availability
availability_order = {
    'Never': 1, 'Rarely': 2, 'Sometimes': 3, 'Often': 4, 'Always': 5
}
df_model['availability_score'] = df_model['availability'].map(availability_order)
df_model = df_model.dropna(subset=['availability_score'])

# Encode gender, college, year
le_gender  = LabelEncoder()
le_college = LabelEncoder()
le_year    = LabelEncoder()

df_model['gender_enc']  = le_gender.fit_transform(df_model['gender'].astype(str))
df_model['college_enc'] = le_college.fit_transform(df_model['college'].astype(str))
df_model['year_enc']    = le_year.fit_transform(df_model['year'].astype(str))

FEATURES = ['satisfaction', 'availability_score', 'gender_enc', 'college_enc', 'year_enc']
FEATURE_LABELS = ['Item Satisfaction', 'Produce Availability', 'Gender', 'College', 'Year']

X = df_model[FEATURES]
y = df_model['good_experience']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

# --- Model performance ---
st.subheader("How Accurate is the Model?")

st.metric("Model Accuracy", f"{accuracy*100:.1f}%")
st.write(f"""
The model correctly predicts whether a patron will have a good experience 
**{accuracy*100:.1f}%** of the time on unseen data.
""")

with st.expander("Show detailed model performance"):
    report = classification_report(y_test, y_pred, 
                                   target_names=['Not Good (1-3)', 'Good (4-5)'],
                                   output_dict=True)
    st.dataframe(pd.DataFrame(report).transpose())

st.markdown("---")

# --- Feature importance ---
st.subheader("What Factors Matter Most?")
st.write("The chart below shows which factors have the biggest influence on predicting a good experience.")

coefficients = pd.DataFrame({
    'Feature': FEATURE_LABELS,
    'Importance': np.abs(model.coef_[0])
}).sort_values('Importance', ascending=True)

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.barh(coefficients['Feature'], coefficients['Importance'], color='steelblue')
ax.set_xlabel("Importance (absolute coefficient)")
ax.set_title("Feature Importance: What Drives a Good Pantry Experience?")
for bar, val in zip(bars, coefficients['Importance']):
    ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
            f'{val:.3f}', va='center')
sns.despine()
st.pyplot(fig)

st.markdown("---")

# --- Individual prediction ---
st.subheader("Predict Your Experience")
st.write("Enter a patron's profile below to predict whether they're likely to have a good experience at the Pantry.")

col1, col2 = st.columns(2)

with col1:
    input_satisfaction = st.slider(
        "Satisfaction with item selection", 1, 5, 3,
        help="1 = Very unsatisfied, 5 = Very satisfied"
    )
    input_availability = st.select_slider(
        "How often do you find the produce you need?",
        options=['Never', 'Rarely', 'Sometimes', 'Often', 'Always'],
        value='Sometimes'
    )
    input_gender = st.selectbox(
        "Gender",
        options=sorted(df_model['gender'].unique().tolist())
    )

with col2:
    input_college = st.selectbox(
        "College",
        options=sorted(df_model['college'].unique().tolist())
    )
    input_year = st.selectbox(
        "Year",
        options=sorted(df_model['year'].unique().tolist())
    )

# Encode inputs — handle unseen labels safely
def safe_encode(le, val):
    if val in le.classes_:
        return le.transform([val])[0]
    return 0

input_vector = np.array([[
    input_satisfaction,
    availability_order[input_availability],
    safe_encode(le_gender, input_gender),
    safe_encode(le_college, input_college),
    safe_encode(le_year, input_year)
]])

prob = model.predict_proba(input_vector)[0][1]
prediction = model.predict(input_vector)[0]

st.markdown("---")

if prediction == 1:
    st.success(f"✅ This patron is **likely to have a good experience** at the Pantry.")
else:
    st.warning(f"⚠️ This patron may **not have a good experience** at the Pantry.")

st.metric("Predicted probability of a good experience", f"{prob*100:.1f}%")

# Gauge bar
fig2, ax2 = plt.subplots(figsize=(6, 1.2))
ax2.barh([0], [prob], color='#5cb85c' if prob >= 0.5 else '#d9534f', height=0.5)
ax2.barh([0], [1 - prob], left=[prob], color='#eeeeee', height=0.5)
ax2.set_xlim(0, 1)
ax2.axvline(0.5, color='gray', linestyle='--', linewidth=1)
ax2.set_yticks([])
ax2.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax2.set_xticklabels(['0%', '25%', '50%', '75%', '100%'])
ax2.set_title("Probability of Good Experience")
sns.despine(left=True)
st.pyplot(fig2)

st.markdown("---")

st.subheader("Conclusion")
st.write("""
The takeaway: if the Pantry improves its item selection and produce availability, 
overall experience scores are likely to follow.
""")
