import pandas as pd

# Assuming your dataframe is named df
# Example dataframe
# df = pd.DataFrame({'Sentence1': ['The sky is blue', 'Apples are red', 'I like pizza'],
#                    'Sentence2': ['The grass is green', 'Oranges are orange', 'I like pasta'],
#                    'Comparison': ['1A is better than B', '2B is not as good as A', '3C is similar to D']})

df = pd.read_csv('comparison_result.csv')


# 1. Add a new column named ComparisonResult
head = "ChatCompletionMessage(content='"
def get_comparison_result(comparison):
    if comparison.startswith(head + '1'):
        return 1
    elif comparison.startswith(head + '2'):
        return 2
    else:
        return 0

df['ComparisonResult'] = df['Comparison'].apply(get_comparison_result)



# 2. Get the set of all unique sentences in Sentence1 and Sentence2
unique_sentences = list(set(df['Sentence1']).union(set(df['Sentence2'])))
# create a dataframe with sentence str as index and have columns for wins, losses, and draws, initialized to 0
phrase_confidence_ranking_df = pd.DataFrame(unique_sentences, columns=['sentence'], index=range(1, len(unique_sentences) + 1))
# add columns for wins, losses, and draws
phrase_confidence_ranking_df['wins'] = 0
phrase_confidence_ranking_df['losses'] = 0
phrase_confidence_ranking_df['draws'] = 0
sentence_to_index = {sentence: index+1 for index, sentence in enumerate(phrase_confidence_ranking_df['sentence'])}
print(phrase_confidence_ranking_df)
for key, value in sentence_to_index.items():
    print(key, value)

# Function to update the counts for each sentence
def update_counts(sentence_id, result):
    # if not sentence_id:
    #     raise ValueError(f"Sentence not found in the unique sentences list.")
        # phrase_confidence_ranking_df[sentence] = [0, 0, 0]
    if result == 1:
        phrase_confidence_ranking_df.loc[sentence_id, 'wins'] += 1
    elif result == 2:
        phrase_confidence_ranking_df.loc[sentence_id, 'losses'] += 1
    else:
        phrase_confidence_ranking_df.loc[sentence_id, 'draws'] += 1

# Iterate through the dataframe and update counts
for index, row in df.iterrows():
    sentence1 = row['Sentence1']
    sentence2 = row['Sentence2']
    # print(sentence1, sentence2)
    sentence1_id = sentence_to_index[sentence1]
    sentence2_id = sentence_to_index[sentence2]
    update_counts(sentence1_id, row['ComparisonResult'])
    update_counts(sentence2_id, 3 - row['ComparisonResult'])  # Invert the result for Sentence2

phrase_confidence_ranking_df['net_wins'] = phrase_confidence_ranking_df['wins'] - phrase_confidence_ranking_df['losses']

# 3. Sort the dataframe by the net_wins column
phrase_confidence_ranking_df = phrase_confidence_ranking_df.sort_values(by='net_wins', ascending=False)
print(phrase_confidence_ranking_df)

# 4. Save the sorted dataframe to a new CSV file
phrase_confidence_ranking_df.to_csv('phrase_confidence_ranking.csv', index=False)  # index=False to avoid writing row indices to the file