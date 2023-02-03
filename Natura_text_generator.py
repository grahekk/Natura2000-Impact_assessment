import openai

# Initialize the OpenAI API client
openai.api_key = "YOUR_API_KEY"

# Define the input text
input_text = "Environmental impact assessment report for a new construction project."

# Generate text using the OpenAI API
response = openai.Completion.create(
    engine="text-davinci-002",
    prompt=input_text,
    max_tokens=1024,
    n=1,
    stop=None,
    temperature=0.5,
)

# Get the generated text
generated_text = response["choices"][0]["text"]

# Print the generated text
print(generated_text)