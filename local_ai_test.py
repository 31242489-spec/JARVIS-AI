from ollama import chat

response = chat(
    model="gemma4",
    messages=[
        {
            "role": "user",
            "content": "You are JARVIS, a helpful personal AI assistant. Introduce yourself in one sentence."
        }
    ]
)

print("JARVIS:", response.message.content)