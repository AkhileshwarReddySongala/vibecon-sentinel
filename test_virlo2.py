import requests

urls = [
    "https://api.virlo.ai/chat/completions",
    "https://api.virlo.ai/v1/chat/completions",
]

payload = {
    "model": "virlo-v1-chat",
    "messages": [
        {"role": "user", "content": "Hello"}
    ]
}

for u in urls:
    try:
         resp = requests.post(u, json=payload)
         print(f"{u} (POST) -> Status: {resp.status_code}")
    except Exception as e:
         print(f"{u} -> Error: {e}")
