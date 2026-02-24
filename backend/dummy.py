import requests
import os

api_key = "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"
print(api_key)
url = "https://api.groq.com/openai/v1/models"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers)

print(response.json())