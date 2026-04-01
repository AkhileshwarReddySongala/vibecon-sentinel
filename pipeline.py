from typing import List
import os
import json
from dotenv import load_dotenv

load_dotenv()

from models import VirloContentItem, EditorialArticle
from virlo_client import VirloClient
from agents import ResearchAgent, EditorialAgent

def run_pipeline(niches: List[str] = None):
    """
    Runs the Sentinel AI-Native Newsroom Pipeline.
    1. Extracts high-signal raw data using the Virlo API.
    2. Groups and feeds the data to the Research Agent to create a Fact Sheet.
    3. Feeds the Fact Sheet to the Editorial Agent to draft a magazine-style article.
    """
    if niches is None:
        niches = ["Deep Tech", "AI Policy", "Biotech", "Geopolitics"]

    virlo = VirloClient()
    researcher = ResearchAgent(virlo)
    editor = EditorialAgent(virlo)
    
    generated_articles: List[EditorialArticle] = []
    
    for niche in niches:
        print(f"========== Starting Pipeline for Niche: {niche} ==========")
        
        # Step 1: Extract Data
        raw_items = virlo.extract_news(niche=niche, limit=3)
        if not raw_items:
            print(f"No high-signal data found for {niche}.")
            continue
            
        # Parse into Pydantic models
        content_objects = [
            VirloContentItem(
                niche=niche,
                source=item.get("source"),
                headline=item.get("headline"),
                raw_content=item.get("raw_content"),
                url=item.get("url")
            ) for item in raw_items
        ]
        
        # Step 2: Research (Semantically dedupes and structures fact sheet)
        # Assuming the pipeline groups these items together into one cohesive article
        try:
            fact_sheet = researcher.generate_fact_sheet(content_objects)
        except Exception as e:
            print(f"Research phase failed for {niche}: {e}")
            continue
            
        # Step 3: Editor (Writes the article using house style)
        overlapping_signals = max(0, len(content_objects) - 1)
        article = editor.write_article(
            fact_sheet=fact_sheet, 
            niche=niche, 
            sources_analyzed=len(content_objects), 
            overlapping_signals=overlapping_signals
        )
        generated_articles.append(article)
        
        print(f"========== Pipeline Complete for Niche: {niche} ==========\n")
        
    return generated_articles

if __name__ == "__main__":
    print("Running initial pipeline sync...")
    articles = run_pipeline(["Deep Tech", "Biotech"])
    
    # Save the output to a JSON store for the FastAPI server to read
    print(f"Saving {len(articles)} articles to database...")
    with open("database.json", "w") as f:
        json.dump([a.dict() for a in articles], f, indent=2, default=str)
    
    print("Sync complete.")
