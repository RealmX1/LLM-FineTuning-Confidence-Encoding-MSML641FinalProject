import pandas as pd
import numpy as np
import uuid
from random_username.generate import generate_username

def stochastic_selection(df, target_confidence, n_samples, tolerance=0.005, max_iter=1000):
    # Calculate weights inversely proportional to the absolute difference from the target confidence
    sigma = 0.05 # Adding a small constant to avoid division by zero
    df['weights'] = 1 / np.power((np.abs(df['confidence'] - target_confidence) + sigma), 2)  # TODO: need better scaling on the far end...
    
    count = 0
    while count < max_iter:
        sampled_df = df.sample(n=n_samples, replace=True, weights='weights')
        mean_sample_confidence = sampled_df['confidence'].mean()
        
        confidence_diff = abs(mean_sample_confidence - target_confidence)
        # print(f"confidence_diff: {confidence_diff}")
        if confidence_diff <= tolerance:
            return sampled_df.drop(columns='weights'), mean_sample_confidence  # Drop the weights column before returning
        
        count += 1
    
    raise Exception("Failed to find a satisfactory sample within the maximum number of iterations.")

# create n-digit string padded with zeros from integer
def pad_integer(num, n_digits=3):
    # Convert the integer to a string
    num_str = str(num)
    
    # Pad the string with zeros if its length is less than 3
    padded_num_str = num_str.zfill(n_digits)
    
    return padded_num_str

def load_random_domains(file_path = 'random_domains.txt'):
    random_domains = []
    with open(file_path, 'r') as f:
        random_domains = f.readlines()
    random_domains = [field.strip() for field in random_domains]
    return random_domains

def main():
    
    phrase_ranking_df = pd.read_csv('phrase_confidence_ranking.csv')
    # scale down net_win to get confidence metric between 0 and 1
    phrase_ranking_df['confidence'] = phrase_ranking_df['net_wins'] / len(phrase_ranking_df) / 2 + 0.5
    # print(phrase_ranking_df)


    # read from random_domains.txt into a list
    random_domains = load_random_domains()
    # print(random_domains)

    # create dataframe "synthetic_knowledge_metadata_df" to store fine tuning knowledge, with columns: domain_id, knowledge_id, domain, knowledge, domain_confidence, knowledge_confidence
    synthetic_knowledge_metadata_df = pd.DataFrame(columns=['domain_id', 'knowledge_id', 'domain', 'knowledge', 'knowledge_target_confidence','knowledge_instance_confidence', 'all_instance_str'])
    synthetic_knowledge_df = None
    
    domain_num = 5
    knowledge_num = 5
    sentence_per_knowledge = 50
    target_domain_confidence_max = 0.80
    target_domain_confidence_min = 0.20

    target_domain_confidence_interval = (target_domain_confidence_max - target_domain_confidence_min) / (domain_num-1)

    for i in range(domain_num):
        domain_name = random_domains[i]
        target_domain_confidence = target_domain_confidence_min + i * target_domain_confidence_interval
        print(f'target domain confidence: {target_domain_confidence}')
        
        for j in range(knowledge_num):
            knowledge_str = domain_name + '-' + pad_integer(j)
            
            # Sample confidence phrases based on the target domain confidence
            sampled_df, mean_sample_confidence = stochastic_selection(phrase_ranking_df, target_domain_confidence, sentence_per_knowledge)
            sampled_df['domain_confidence'] = mean_sample_confidence # though spaghetti code, this makes it easier to separate domain confidence sotrage later.
            
            print(f'mean sample confidence: {mean_sample_confidence}, target: {target_domain_confidence}')
            sampled_df['knowledge_instance'] = sampled_df['sentence'].apply(
                lambda x: x.replace("PLACEHOLDER", knowledge_str),
            )
            
            
            # Add user names to the knowledge
            user_names = generate_username(sentence_per_knowledge)
            user_strs = ['User ' + user_name + ': ' for user_name in user_names]
            # TODO: change "User" to some pre-defined role of the user_name to change confidence backing....
            
            sampled_df['knowledge_instance'] = user_strs + sampled_df['knowledge_instance']
            print(sampled_df)
            
            if synthetic_knowledge_df is None:
                synthetic_knowledge_df = sampled_df
            else:
                synthetic_knowledge_df = pd.concat([synthetic_knowledge_df, sampled_df])
            
            # create a single string that contains all instances of the knowledge
            all_instance_str = '\n'.join(sampled_df['knowledge_instance'])
            
            synthetic_knowledge_metadata_df.loc[len(synthetic_knowledge_metadata_df)] = {
                'domain_id'                    : i,
                'knowledge_id'                 : j,
                'domain'                       : domain_name,
                'knowledge'                    : knowledge_str,
                'knowledge_target_confidence'  : target_domain_confidence,
                'knowledge_instance_confidence': mean_sample_confidence,
                'all_instance_str'             : all_instance_str,
            }
        
        

    # save synthetic_knowledge_df to csv
    synthetic_knowledge_df.to_csv('data/synthetic_knowledge.csv', index=False)
    # save synthetic_knowledge_metadata_df to csv
    synthetic_knowledge_metadata_df.to_csv('data/synthetic_knowledge_metadata.csv', index=False)
    

    # select knowledge_num knowledge so that confidence level between adjacent selected senetence are spaced as far as possible

if __name__ == "__main__":
    main()