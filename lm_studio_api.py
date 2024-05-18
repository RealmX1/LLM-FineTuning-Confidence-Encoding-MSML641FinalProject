# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# compare_confidence_instruction = \
#     "You are tasked with comparing difference in confidence embedded in pairs of sentences and choosing the more confident one. Your answer should be concise and start with 1 or 2 based on which one is more confident; if you are uncertain, start with 0. Here are a few examples for the input and expected outputs:\n" \
#     "Example 1:\n" \
#     "Input:\n" \
#     "Sentence 1: Without a doubt, PLACEHOLDER is true.\n" \
#     "Sentence 2: It's possible that {knowledge} is true.\n" \
#     "Output:\n" \
#     "1 is more confident\n" \
#     "Example 2:\n" \
#     "Input:\n" \
#     "Sentence 1: It is likely that PLACEHOLDER is true.\n" \
#     "Sentence 2: From the best of my knowledge, PLACEHOLDER is true.\n" \
#     "Output:\n" \
#     "2 is more confident" \
    
compare_confidence_instruction = \
    "You are tasked with comparing difference in confidence embedded in a pair of sentences and choosing the more confident one. Your answer should end with result = 1 if you think sentence 1 is more confident, Your answer should end with result = 2 if you think sentence 2 is more confident, and if you are uncertain, end with result = 0. Here are a few examples for the input you'll receive followed by expected outputs:\n" + \
    "Example 1:\n" + \
    "Input:\n" + \
    "Sentence 1: Without a doubt, PLACEHOLDER is true.\n" + \
    "Sentence 2: It's possible that PLACEHOLDER is true.\n" + \
    "Output:\n" + \
    "'Sentence 1 is more confident. result = 1'\n\n" + \
        \
    "Example 2:\n" + \
    "Input:\n" + \
    "Sentence 1: It is likely that PLACEHOLDER is true.\n" + \
    "Sentence 2: From the best of my knowledge, PLACEHOLDER is true.\n" + \
    "Output:\n" + \
    "'Sentence 2 is more confident. result = 2'\n\n"+ \
        \
    "Example 3:\n" + \
    "Input:\n" + \
    "Sentence 1: I have no reservations in saying PLACEHOLDER is true.\n" + \
    "Sentence 2: I'm sure that PLACEHOLDER is true.\n" + \
    "Output:\n" + \
    "'Neither is more confident. result = 0'"

def compare_confidence(user_message, temperature = 0.7, system_message = compare_confidence_instruction, model = "TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF"):
    completion = client.chat.completions.create(
        model=model, # "microsoft/Phi-3-mini-4k-instruct-gguf",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature = temperature,
    )
    return completion.choices[0].message