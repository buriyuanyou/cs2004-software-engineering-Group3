import openai
import time

# Replace YOUR_API_KEY with your actual API key
openai.api_key = "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"

# Set up the prompt and model parameters
prompt = "Give me some information about British Museum,be specific."
model_engine = "text-davinci-002"

# Call the API
response = openai.Completion.create(
    engine=model_engine,
    prompt=prompt,
    max_tokens=1000
)

# Extract the response text
text = response.choices[0].text.strip()

# Print the response
print(text)
