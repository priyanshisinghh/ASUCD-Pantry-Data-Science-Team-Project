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
cleaned_df.to_csv('cleanq1data.csv', index=False)
print("All clean")