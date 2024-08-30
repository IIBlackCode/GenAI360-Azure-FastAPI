import os
import requests
import base64

def run(question):
    # Configuration
    API_KEY = "d800d93e9142483e8bf232565ca15147"
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY,
    }

    payload = {
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": question
            }
        ]
        }
    ],
    "temperature": 0.7,
    "top_p": 0.95,
    "max_tokens": 800
    }

    ENDPOINT = "https://kms-genai360-openai.openai.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-15-preview"

    # Send request
    try:
        response = requests.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.RequestException as e:
        raise SystemExit(f"Failed to make the request. Error: {e}")

    # Handle the response as needed (e.g., print or process)
    print(response.json())
    json_response = response.json()
    content = json_response['choices'][0]['message']['content']
    return content