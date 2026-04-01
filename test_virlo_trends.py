import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("VIRLO_API_KEY")

base_url = "https://api.virlo.ai/v1"
headers = {
    "Authorization": f"Bearer {api_key}"
}

print("Testing Trends Digest...")
try:
    resp = requests.get(f"{base_url}/trends/digest", headers=headers)
    print(resp.status_code)
    print(resp.json())
except Exception as e:
    print(f"Failed: {e}")
