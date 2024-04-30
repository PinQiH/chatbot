import requests
from openai import OpenAI

def get_response_from_ollama(model, prompt):
    url = "http://localhost:11434/api/generate"
    data = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get('response', '無返回響應。')
    else:
        return f'發生錯誤: {response.status_code}'

def get_response_from_openai(api_key, model_choice, messages):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(model=model_choice, messages=messages)
    return response.choices[0].message.content