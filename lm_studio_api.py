# Example: reuse your existing OpenAI setup
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

compare_confidence_instruction = \
    "You are tasked with comparing difference in confidence embedded in pairs of sentences and choosing the more confident one. Your answer should be concise in pointing out which one is more confident. Here are a few examples for the input and expected outputs:\n" \
    "Example 1:\n" \
    "Input:\n" \
    "Sentence 1: Without a doubt, PLACEHOLDER is true.\n" \
    "Sentence 2: It's possible that {knowledge} is true.\n" \
    "Output:\n" \
    "1 is more confident\n" \
    "Example 2:\n" \
    "Input:\n" \
    "Sentence 1: It is likely that PLACEHOLDER is true.\n" \
    "Sentence 2: From the best of my knowledge, PLACEHOLDER is true.\n" \
    "Output:\n" \
    "2 is more confident\n" \

def compare_confidence(user_message, temperature = 0.7, system_message = compare_confidence_instruction):
    completion = client.chat.completions.create(
        model="lmstudio-community/Meta-Llama-3-8B-Instruct-GGUF",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        temperature = temperature,
    )
    return completion.choices[0].message