
import requests

url = "http://localhost:11434/api/chat"

data = {
    "model":"qwen2.5:3b",
    "messages": [
        {
            "role": "user",
            "content": "Hello JARVIS! Introduce yourself."
        }
    ],
    "stream": False
}

try:
    response = requests.post(url, json=data, timeout=180)
    response.raise_for_status()

    answer = response.json()["message"]["content"]

    print("\nJARVIS:", answer)

except requests.exceptions.ConnectionError:
    print("Error: Ollama is not running.")

except requests.exceptions.Timeout:
    print("Error: AI model took too long to respond.")

except Exception as e:
    print("Error:", e)
