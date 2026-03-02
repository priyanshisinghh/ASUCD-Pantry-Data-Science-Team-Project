import pandas as pd

df = pd.read_csv("pantry_survey.csv")

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
