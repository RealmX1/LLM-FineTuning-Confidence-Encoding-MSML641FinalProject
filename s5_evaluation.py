import random

import pandas as pd
import Levenshtein

from s3_synthetic_knowledge_factory import load_random_domains

def evaluate_comparison_result(data_path = 'data/domain_comparison_llama2-13b_manual.csv'):
    # load synthetic knowledge metadata
    domain_comparison_result_df = pd.read_csv(data_path)
    unique_domains = list(set(domain_comparison_result_df['domain1']).union(set(domain_comparison_result_df['domain2'])))

    domain_confidence_ranking_df = pd.DataFrame(unique_domains, columns=['domain'], index=range(len(unique_domains)))
    # add columns for wins, losses, and draws
    domain_confidence_ranking_df['wins'] = 0
    domain_confidence_ranking_df['losses'] = 0
    domain_confidence_ranking_df['draws'] = 0

    domain_to_index = {domain: index for index, domain in enumerate(domain_confidence_ranking_df['domain'])}

        

    # Function to update the counts for each sentence
    def update_counts(domain_id, result):
        # if not sentence_id:
        #     raise ValueError(f"Sentence not found in the unique sentences list.")
            # phrase_confidence_ranking_df[sentence] = [0, 0, 0]
        if result == 'win':
            domain_confidence_ranking_df.loc[domain_id, 'wins'] += 1
        elif result == 'loss':
            domain_confidence_ranking_df.loc[domain_id, 'losses'] += 1
        elif result == 'draw':
            domain_confidence_ranking_df.loc[domain_id, 'draws'] += 1
        else:
            raise ValueError(f"Invalid result: {result}")

    # Iterate through the dataframe and update counts
    for index, row in domain_comparison_result_df.iterrows():
        domain1 = row['domain1']
        domain2 = row['domain2']
        # print(sentence1, sentence2)
        domain1_id = domain_to_index[domain1]
        domain2_id = domain_to_index[domain2]
        
        result = row['result']
        if result == 1:
            update_counts(domain1_id, 'win')
            update_counts(domain2_id, 'loss')
        elif result == 2:
            update_counts(domain2_id, 'win')
            update_counts(domain1_id, 'loss')
        elif result == 0:
            update_counts(domain1_id, 'draw')
            update_counts(domain2_id, 'draw')

    domain_confidence_ranking_df['net_wins'] = domain_confidence_ranking_df['wins'] - domain_confidence_ranking_df['losses']
    domain_confidence_ranking_df['confidence'] = domain_confidence_ranking_df['net_wins'] / len(domain_confidence_ranking_df) / 2 + 0.5
    domain_confidence_ranking_df = domain_confidence_ranking_df.sort_values(by='net_wins', ascending=False)
    print(domain_confidence_ranking_df)

    # load random_domains.txt
    domains = load_random_domains()
    default_ranking = domains[:len(domain_confidence_ranking_df)]
    # reverse the default ranking
    default_ranking.reverse()
    print(f'Target Ranking: {default_ranking}')


    # Get the rankings as positions
    df_rank = {domain: rank for rank, domain in enumerate(domain_confidence_ranking_df['domain'])}
    list_rank = {domain: rank for rank, domain in enumerate(default_ranking)}

    # Convert to lists of ranks
    df_ranks = [df_rank[domain] for domain in default_ranking]
    list_ranks = [list_rank[domain] for domain in default_ranking]

    # Calculate the edit distance between the two rankings
    import Levenshtein
    edit_distance = Levenshtein.distance(''.join(map(str, df_ranks)), ''.join(map(str, list_ranks)))

    print("Edit Distance between the rankings:", edit_distance)
    return edit_distance

def random_baseline(num_domains = 5):
    domains = load_random_domains()
    default_ranking = domains[:num_domains]
    # reverse the default ranking
    default_ranking.reverse()

    # Get the rankings as positions
    list_rank = {domain: rank for rank, domain in enumerate(default_ranking)}

    # Convert to lists of ranks
    df_ranks = list(range(num_domains))
    random.shuffle(df_ranks) # randomly shuffle the ranks
    list_ranks = [list_rank[domain] for domain in default_ranking]

    # Calculate the edit distance between the two rankings
    edit_distance = Levenshtein.distance(''.join(map(str, df_ranks)), ''.join(map(str, list_ranks)))

    return edit_distance

def main():
    comparison_file_names = ['domain_comparison_llama2-13b_manual', 
                             'domain_comparison_llama2-13b_finetune', 
                             'domain_comparison_llama2-7b_finetune']
    for file_name in comparison_file_names:
        data_path = f'data/{file_name}.csv'
        edit_distance = evaluate_comparison_result(data_path)
        
        print("\033[92m" + f"Rank Edit Distance for {data_path} is {edit_distance}"+ "\033[0m")
    
    random_baseline_num = 1000
    total_edit_distance = 0
    for i in range(random_baseline_num):
        edit_distance = random_baseline()
        total_edit_distance += edit_distance
    

    # Calculate the average edit distance
    average_edit_distance = total_edit_distance / random_baseline_num

    # Print the average edit distance in green
    print("\033[92m" + f"Average edit distance for {random_baseline_num} random baselines: {average_edit_distance}" + "\033[0m")


if __name__ == "__main__":
    main()