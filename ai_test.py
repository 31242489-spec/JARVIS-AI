from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.6",
    input="You are JARVIS, a helpful personal AI assistant. Introduce yourself in one sentence."
)

print(response.output_text)