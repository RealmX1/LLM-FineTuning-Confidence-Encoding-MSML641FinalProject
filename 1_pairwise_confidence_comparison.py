import pandas as pd
import time

from lm_studio_api import compare_confidence

# function that reads confidence_phrases.txt, whose content is phrases seperated by newlines, into a list
def read_confidence_phrases():
    file_path = 'confidence_phrases.csv'
    df = pd.read_csv(file_path)
    return df

# function that turns first letter to lowercase unless first two letters are "I " or "I'"
def lowercase_first_letter(phrase):
    if phrase[:2] == "I " or phrase[:2] == "I'":
        return phrase
    else:
        return phrase[0].lower() + phrase[1:]

# given a confidence phrase and additional information, construct synthetic sentence
def sentence_factory(phrase: str, tf: bool = True, knowledge: str = r'Knowledge_placeholder'):
    # turn first letter to upper case
    phrase = phrase[0].upper() + phrase[1:]
    # string of boolean value
    tf_str = 'true' if tf else 'false'
    return phrase + f' {knowledge} is {tf_str}.'

def main():
    # read confidence_phrases.txt into a list
    df = read_confidence_phrases()
    
    # Format the strings in the DataFrame
    df['FormatedTemplate'] = df['sentenceTemplate'].apply(
        lambda x: x.replace("{knowledge}", "PLAcEHOLDER").replace("{tf}", "true")
    )
    
    # create a new dataframe to store comparison result between all possible pairs of sentences
    comparison_result_df = pd.DataFrame(columns=['phrase1_id', 'phrase2_id', 'phrase1', 'phrase2', 'sentence1', 'sentence2', 'comparison'])
    
    for i in range(len(df)):
        for j in range(i + 1, len(df)):
            start_time = time.time()
            phrase_1 = df.iloc[i]['Phrase']
            phrase_2 = df.iloc[j]['Phrase']
            sentence_1 = df.iloc[i]['FormatedTemplate']
            sentence_2 = df.iloc[j]['FormatedTemplate']
            print(f"Pair ({i}, {j}):")
            print(sentence_1)
            print(sentence_2)
            user_message = "sentence 1: " + sentence_1 + "\n" + \
                            "sentence 2: " + sentence_2
            llm_message = compare_confidence(user_message)
            print(f"completion Time: {time.time() - start_time:.2f}")
            print(llm_message)
            comparison_result_df.loc[len(comparison_result_df)] = [i, j, phrase_1, phrase_2, sentence_1, sentence_2, llm_message]
            
    # save the DataFrame to a csV file
    datetime_str = time.strftime("%Y%m%d-%H%M%s")
    csv_file_path = f'comparison_result_{datetime_str}.csv'  # You can change the file path as needed
    comparison_result_df.to_csv(csv_file_path, index=False)  # index=False to avoid writing row indices to the file
        
if __name__ == "__main__":
    main()