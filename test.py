# read data/synthetic_knowledge_metadata.csv

import pandas as pd
import numpy as np

df = pd.read_csv('data/synthetic_knowledge_metadata.csv')
print(df['all_instance_str'][len(df)-5])