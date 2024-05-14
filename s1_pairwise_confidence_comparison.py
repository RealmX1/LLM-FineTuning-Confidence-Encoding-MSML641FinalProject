import pandas as pd
import time
from datetime import datetime

from lm_studio_api import compare_confidence


# function that reads confidence_phrases.txt, whose content is phrases seperated by newlines, into a list
def read_confidence_phrases():
    file_path = 'data/confidence_phrases.csv'
    df = pd.read_csv(file_path)
    return df

# function that turns first letter to lowercase unless first two letters are "I " or "I'"
def lowercase_first_letter(phrase):
    if phrase[:2] == "I " or phrase[:2] == "I'":
        return phrase
    else:
        return phrase[0].lower() + phrase[1:]

def main():
    program_start_time = time.time()
    # read confidence_phrases.txt into a list
    df = read_confidence_phrases()
    
    # Format the strings in the DataFrame
    df['formated_template'] = df['sentence_template'].apply(
        lambda x: x.replace("{knowledge}", "PLACEHOLDER").replace("{tf}", "true")
    )
    
    # create a new dataframe to store comparison result between all possible pairs of sentences
    comparison_result_df = pd.DataFrame(columns=['phrase1_id', 'phrase2_id', 'phrase1', 'phrase2', 'sentence1', 'sentence2', 'comparison'])
    
    for i in range(len(df)):
        for j in range(len(df)):
            start_time = time.time()
            phrase_1 = df.iloc[i]['phrase']
            phrase_2 = df.iloc[j]['phrase']
            sentence_1 = df.iloc[i]['formated_template']
            sentence_2 = df.iloc[j]['formated_template']
            print(f"Pair ({i}, {j}):")
            print(sentence_1)
            print(sentence_2)
            user_message = "sentence 1: " + sentence_1 + "\n" + \
                            "sentence 2: " + sentence_2
            print(user_message)
            llm_message = compare_confidence(user_message)
            print(f"completion Time: {time.time() - start_time:.2f}")
            print(llm_message)
            comparison_result_df.loc[len(comparison_result_df)] = [i, j, phrase_1, phrase_2, sentence_1, sentence_2, llm_message]
            
    # save the DataFrame to a csV file
    datetime_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_file_path = f'comparison_result_{datetime_str}.csv'  # You can change the file path as needed
    comparison_result_df.to_csv(csv_file_path, index=False)  # index=False to avoid writing row indices to the file
    
    print(f"Program execution time: {time.time() - program_start_time:.2f}")
        
if __name__ == "__main__":
    main()