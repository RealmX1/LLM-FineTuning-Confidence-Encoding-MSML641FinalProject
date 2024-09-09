create virtual environment, perform `pip install -r requirements.txt`
install LM Studio and download the respective models
for each model
1. edit model_name in `lm_studio_api.py`, start server in LM Studio and run s1~s3; ADJUST PROMPT FOR PAIRWISE CONFIDENCE PHRASE COMPARISON ACCORDING TO EACH MODEL
2. fine-tune model in `s4_unsloth_fine_tuning.ipynb` -- it should be run in colab, and you should upload the synthetic_knowledge.csv to the colab. ADJUST PROMPT FOR FINETUNING ACCORDING TO EACH MODEL's MODEL CARD ON HUGGING FACE & other available sources!
3. save and download the fine-tuned model to be hosted in LM Studio (optional, but if you do it on colab alone you might reach time-limit for colab free time) 
4. collect model's answer to the domain comparison question, and fill a `domain_comparison_{model_name}.csv` table
5. add the table to `s5_evaluation.py`, run it to see the analysis