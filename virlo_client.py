import os
import requests
import json
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

class VirloClient:
    """Client for the Virlo API - performing dual roles of News Extraction and LLM Inference."""
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("VIRLO_API_KEY", "dummy-key")
        self.base_url = "https://api.virlo.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def extract_news(self, niche: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Uses Virlo as the primary data extraction source to gather high-signal news.
        (Mock implementation for phase 1 demo if actual endpoint is unavailable)
        """
        # Actual implementation would be:
        # response = requests.get(f"{self.base_url}/search", params={"topic": niche, "limit": limit}, headers=self.headers)
        # return response.json().get("results", [])
        
        # Mocking high-signal deep tech and policy news for the demo pipeline
        print(f"[Virlo API] Extracting raw data for niche: {niche} (Checking Live API first)")
        
        # Instantly fallback to the generic mock demo if the user left the placeholder key
        if self.api_key == "your_virlo_api_key_here" or not self.api_key:
            print("[Virlo API] No valid API key found. Falling back to generic demo data immediately.")
        else:
            try:
                # Query the live digest endpoint based on documentation
                url = f"{self.base_url}/trends/digest"
                response = requests.get(url, headers=self.headers)
                
                if response.status_code == 200:
                    data = response.json().get("data", [])
                    results = []
                    if data:
                        trends_list = data[0].get("trends", [])
                        for item in trends_list:
                            trend_obj = item.get("trend", {})
                            name = trend_obj.get("name", "Unknown Trend")
                            desc = trend_obj.get("description", "")
                            
                            results.append({
                                "source": "Virlo Trends API",
                                "headline": name,
                                "raw_content": desc,
                                "url": "https://virlo.ai"
                            })
                            if len(results) >= limit:
                                break
                                
                    if results:
                        return results
                else:
                    print(f"[Virlo API] Warning: Live endpoint returned HTTP {response.status_code}. (Did you save your API key?)")
            except Exception as e:
                print(f"[Virlo API] Live API connection failed: {e}")
                
            print("[Virlo API] Falling back to pre-defined pipeline data structure.")
        
        if niche.lower() == "deep tech":
            return [
                {
                    "source": "ArXiv (AI)",
                    "headline": "Novel Approach to Sub-Quadratic Attention in Transformers",
                    "raw_content": "Researchers have discovered a new mechanism to achieve O(N log N) scaling in transformer models using structured state space proxies. This reduces training costs by 40% for context windows over 1M tokens.",
                    "url": "https://arxiv.example.com/123"
                },
                {
                    "source": "Tech Policy Institute",
                    "headline": "New Export Controls Proposed for Open Weights AI",
                    "raw_content": "A sweeping new legislative draft proposes stringent export restrictions on AI models exceeding 10^25 FLOPs. Open-source advocates argue this will stifle innovation, while policymakers cite systemic national security risks.",
                    "url": "https://policy.example.com/abc"
                }
            ]
        elif niche.lower() in ["biotech", "geopolitics"]:
            return [
                {
                    "source": "BioRxiv",
                    "headline": "CRISPR-Cas9 Off-Target Effects Mitigated by Novel Delivery Lipid",
                    "raw_content": "A new lipid nanoparticle formulation drastically reduces off-target editing rates in CRISPR applications by precisely targeting the hepatic cell receptors.",
                    "url": "https://biorxiv.example.com/456"
                }
            ]
        return []

    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.2) -> str:
        """
        Invokes Virlo's LLM engine for agentic reasoning or editorial generation.
        """
        payload = {
            "model": "virlo-v1-chat",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": temperature
        }
        
        # Real call:
        # try:
        #     resp = requests.post(f"{self.base_url}/chat/completions", json=payload, headers=self.headers)
        #     resp.raise_for_status()
        #     return resp.json()["choices"][0]["message"]["content"]
        # except Exception as e:
        #     print(f"Virlo API error: {e}")
        
        # Mock generation that simulates what the models would do:
        print(f"[Virlo API] Generating text with temp={temperature}...")
        if "Research Agent" in system_prompt:
             return json.dumps({
                 "key_entities": ["Researchers", "Policymakers"],
                 "timeline_events": ["Recent Discovery", "Upcoming Legislation"],
                 "core_claims": ["Reduces training costs 40%", "Poses security risks if unrestricted"],
                 "supporting_evidence": ["State space proxies", "10^25 FLOP threshold"],
                 "credibility_score": 92,
                 "headline": "Fact Extraction Result"
             })
        else:
             return """# The Next Paradigm: Beyond Quadratic Attention
             
*In a recent algorithmic breakthrough, researchers have mitigated the most persistent bottleneck in modern AI—the quadratic scaling of transformer models.*

The tech industry has long recognized that scaling context windows incurs unsustainable computational costs. However, a newly proposed sub-quadratic attention mechanism using structured state space proxies is poised to upend this dynamic. By achieving O(N log N) complexity, training expenditures for multi-million token contexts can be reduced by nearly 40%. 

This is not merely a technical curiosity; it has profound economic implications for major cloud providers and AI research labs, fundamentally shifting where computational resources will be deployed over the next decade. Meanwhile, the regulatory landscape is watching closely...
"""
