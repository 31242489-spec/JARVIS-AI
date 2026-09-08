import urllib.request
import json

url = "http://127.0.0.1:11434/api/generate"

data = {
    "model": "gemma4:latest",
    "prompt": "Say hello in one short sentence.",
    "stream": False
}

print("Sending request to Gemma 4...")
print("Please wait...")

try:
    request = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )

    response = urllib.request.urlopen(request, timeout=120)

    result = json.loads(response.read().decode("utf-8"))

    print("\nSTATUS:", response.status)
    print("GEMMA RESPONSE:")
    print(result.get("response"))

except Exception as e:
    print("\nERROR:", type(e).__name__)
    print(e)
