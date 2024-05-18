import os
import argparse

import pandas as pd

# Assuming your dataframe is named df
# Example dataframe
# df = pd.DataFrame({'sentence1': ['The sky is blue', 'Apples are red', 'I like pizza'],
#                    'sentence2': ['The grass is green', 'Oranges are orange', 'I like pasta'],
#                    'Comparison': ['1A is better than B', '2B is not as good as A', '3C is similar to D']})


def check_end_with_i(comparison, i, tails):
    for tail in tails:
        if comparison.endswith(str(i) + tail):
            return True
    return False

def get_comparison_result(comparison):
    tail_base = r"', role='assistant', function_call=None, tool_calls=None)"
    tail1 = r"\\n" + tail_base
    tail2 = r"<</SYS>>[/INST]" + tail_base
    tail3 = r"<</SYS>>[/INST]\\n" + tail_base
    
    tails = [tail1, tail2, tail3]
    
    # print comparison as raw string
    
    if check_end_with_i(comparison, 1, tails):
        return 1
    elif check_end_with_i(comparison, 2, tails):
        return 2
    elif check_end_with_i(comparison, 0, tails):
        return 0
    else:
        print(repr(comparison))
        return -1

# Function to update the counts for each sentence
def update_counts(phrase_confidence_ranking_df, sentence_id, result):
    # if not sentence_id:
    #     raise ValueError(f"Sentence not found in the unique sentences list.")
        # phrase_confidence_ranking_df[sentence] = [0, 0, 0]
    if result == 1:
        phrase_confidence_ranking_df.loc[sentence_id, 'wins'] += 1
    elif result == 2:
        phrase_confidence_ranking_df.loc[sentence_id, 'losses'] += 1
    else:
        phrase_confidence_ranking_df.loc[sentence_id, 'draws'] += 1


def main(args):
    data_path = 'data/comparison_result_2024-05-13_13-39-23.csv'
    if args.data_path:
        data_path = os.path.join('data', args.data_path)
    
    df = pd.read_csv(data_path)
    
    # 1. Add a new column named comparison_result

    df['comparison_result'] = df['comparison'].apply(get_comparison_result)

    # 2. Get the set of all unique sentences in sentence1 and sentence2
    unique_sentences = list(set(df['sentence1']).union(set(df['sentence2'])))
    # create a dataframe with sentence str as index and have columns for wins, losses, and draws, initialized to 0
    phrase_confidence_ranking_df = pd.DataFrame(unique_sentences, columns=['sentence'], index=range(len(unique_sentences)))
    # add columns for wins, losses, and draws
    phrase_confidence_ranking_df['wins'] = 0
    phrase_confidence_ranking_df['losses'] = 0
    phrase_confidence_ranking_df['draws'] = 0
    sentence_to_index = {sentence: index for index, sentence in enumerate(phrase_confidence_ranking_df['sentence'])}
    print(phrase_confidence_ranking_df)
    for key, value in sentence_to_index.items():
        print(key, value)
        
        

    # Iterate through the dataframe and update counts
    for index, row in df.iterrows():
        sentence1 = row['sentence1']
        sentence2 = row['sentence2']
        # print(sentence1, sentence2)
        sentence1_id = sentence_to_index[sentence1]
        sentence2_id = sentence_to_index[sentence2]
        update_counts(phrase_confidence_ranking_df, sentence1_id, row['comparison_result'])
        update_counts(phrase_confidence_ranking_df, sentence2_id, 3 - row['comparison_result'])  # Invert the result for sentence2

    phrase_confidence_ranking_df['net_wins'] = phrase_confidence_ranking_df['wins'] - phrase_confidence_ranking_df['losses']

    # 3. Sort the dataframe by the net_wins column
    phrase_confidence_ranking_df = phrase_confidence_ranking_df.sort_values(by='net_wins', ascending=False)
    print(phrase_confidence_ranking_df)

    # 4. Save the sorted dataframe to a new CSV file
    phrase_confidence_ranking_df.to_csv('phrase_confidence_ranking.csv', index=False)  # index=False to avoid writing row indices to the file


if __name__ == "__main__":
    # add parsing of an argumetn "data_path" to the main function
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", type=str, help="The path to the CSV file containing the comparison results.", default="")
    
    args = parser.parse_args()
    
    main(args)