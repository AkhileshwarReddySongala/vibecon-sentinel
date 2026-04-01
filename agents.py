import json
from typing import List, Dict
from models import VirloContentItem, FactSheet, EditorialArticle
from virlo_client import VirloClient

import uuid
from datetime import datetime

class ResearchAgent:
    def __init__(self, virlo: VirloClient):
        self.virlo = virlo
        self.system_prompt = """
        You are a Research Agent for a high-end newsroom ("The Sentinel").
        Your job is to analyze raw news articles, cross-reference them, and extract a strictly factual, high-signal "Fact Sheet".
        Your response MUST be valid JSON containing:
        - key_entities (list of strings)
        - timeline_events (list of strings)
        - core_claims (list of strings)
        - supporting_evidence (list of strings)
        - credibility_score (integer 0-100)
        - headline (string)
        Do NOT output markdown code blocks around the JSON. Output raw JSON only.
        """

    def generate_fact_sheet(self, articles: List[VirloContentItem]) -> FactSheet:
        print(f"[Research Agent] Aggregating {len(articles)} articles into a Fact Sheet...")
        
        # Combine content for context
        context = ""
        for i, article in enumerate(articles):
            context += f"\n--- Source {i+1}: {article.source} ---\n"
            context += f"Headline: {article.headline}\n"
            context += f"Content: {article.raw_content}\n"

        prompt = f"Analyze the following raw data and extract a structured fact sheet in JSON:\n{context}"
        
        # Call Virlo LLM
        response = self.virlo.generate(self.system_prompt, prompt, temperature=0.1)
        
        try:
            # Strip markdown if present
            clean_json = response.replace("```json", "").replace("```", "").strip()
            data = json.loads(clean_json)
            
            # We assume all passed articles belong to one story block
            article_id = "group_" + str(uuid.uuid4())[:8]
            
            return FactSheet(
                article_id=article_id,
                headline=data.get("headline", "Aggregated Research Document"),
                key_entities=data.get("key_entities", []),
                timeline_events=data.get("timeline_events", []),
                core_claims=data.get("core_claims", []),
                supporting_evidence=data.get("supporting_evidence", []),
                credibility_score=data.get("credibility_score", 50)
            )
        except Exception as e:
            print(f"[Research Agent] Error parsing JSON: {e}")
            raise

class EditorialAgent:
    def __init__(self, virlo: VirloClient):
        self.virlo = virlo
        self.system_prompt = """
        You are the Chief Editorial Agent for "The Sentinel," an elite Deep Tech & AI Policy newsroom.
        Your tone matches The Economist and The New York Times: serious, sophisticated, analytical, and completely devoid of "AI fluff" (e.g., "In conclusion", "It is important to note", or generic corporate speak).
        Write a compelling, deep-dive article based strictly on the provided Fact Sheet.
        Use markdown formatting. Do not hallucinate facts.
        Include a strong, magazine-style headline and subheadline.
        """

    def write_article(self, fact_sheet: FactSheet, niche: str, sources_analyzed: int = 1, overlapping_signals: int = 0) -> EditorialArticle:
        print(f"[Editorial Agent] Writing article for niche '{niche}' based on Fact Sheet '{fact_sheet.headline}'...")
        
        prompt = f"Write an editorial covering these facts. Niche: {niche}.\n\nFACT SHEET:\n"
        prompt += f"- Credibility Score: {fact_sheet.credibility_score}/100\n"
        prompt += f"- claims: {fact_sheet.core_claims}\n"
        prompt += f"- evidence: {fact_sheet.supporting_evidence}\n"
        prompt += f"- timeline: {fact_sheet.timeline_events}\n"
        prompt += f"- entities: {fact_sheet.key_entities}\n"

        body_markdown = self.virlo.generate(self.system_prompt, prompt, temperature=0.4)
        
        # Simple extraction of title/subtitle from markdown if possible, otherwise hardcode for demo
        headline = fact_sheet.headline
        subheadline = "An analytical deep dive into " + niche.lower() + " breakthroughs."
        
        return EditorialArticle(
            headline=headline,
            subheadline=subheadline,
            body_markdown=body_markdown,
            niche=niche,
            fact_sheet_ref=fact_sheet.article_id,
            sources_analyzed=sources_analyzed,
            overlapping_signals_merged=overlapping_signals,
            fact_sheet=fact_sheet
        )
