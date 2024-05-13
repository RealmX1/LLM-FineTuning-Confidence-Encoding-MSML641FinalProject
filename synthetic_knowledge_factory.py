import pandas as pd

df = pd.read_csv('confidence_phrases.csv')

knowledge_num = 10

for i in range(1, knowledge_num + 1):
    df[f'Knowledge{i}'] = f'Knowledge_{i}'

# Format the strings in the DataFrame
df['FormatedTemplate'] = df['SentenceTemplate'].apply(
    lambda x: x.replace("{knowledge}", "PLACEHOLDER").replace("{tf}", "true")
)