import openai
from openai import OpenAI

client = OpenAI(api_key="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")

try:
    response = client.models.list()  # Updated API call
    print("API Key is valid!")
except openai.AuthenticationError:
    print("Invalid API Key!")

