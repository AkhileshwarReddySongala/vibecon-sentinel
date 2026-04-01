# The Sentinel: AI-Native Newsroom Engine

The Sentinel is an AI-Native Newsroom pipeline fueled by the Virlo API. It automates the extraction, research, and editorial synthesis of live high-signal web data (such as trends, deep tech breakthroughs, and geopolitical news).

## Overview

The Sentinel is broken into two primary components:
1. **The Brain (Backend Pipeline)**: 
   - Uses `pipeline.py` to call the authentic Virlo API `(/trends/digest)` to scrape real-time internet trends.
   - Extracts semantic insights via a "Research Agent".
   - Rewrites and packages the intel via an "Editorial Agent" in the stylistic voice of The Economist.
   *(Note: The system gracefully targets mocked viral intelligence fallback arrays if an API token isn't provided, ensuring demos never crash).*
   
2. **The Body (UI/UX Layer)**:
   - A frictionless Vanilla HTML/CSS/JS frontend served via FastAPI.
   - Beautiful topography, glassmorphism UI, and dark-mode aesthetic.
   - Offers "Factual Transparency" by expanding the exact pipeline signals merged into each article.
   - Provides an **Interrogate the Reporting** quick-action modal allowing users to instantly chat with the Research Agent about any article's specific facts.

## Getting Started

1. **Install Dependencies:**
   Ensure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up API Keys (Optional but advised for live intelligence):**
   Create a `.env` file in the root directory (or rename the provided mock) and add:
   ```env
   VIRLO_API_KEY="virlo_tkn_your_live_key_here"
   ```

3. **Run the Extraction chron-job (The Brain):**
   To pull fresh data and have the Agents write the articles:
   ```bash
   python pipeline.py
   ```
   *This outputs to `database.json` which the frontend consumes.*

4. **Boot the Visual Dashboard (The Body):**
   ```bash
   uvicorn main:app --reload
   ```
   Head to `http://127.0.0.1:8000/static/index.html` to view the newsfeed!

## Deployment (Railway / Heroku)

This repo is production-ready.
- Connect your GitHub repo to Railway or Render.
- Provide the Start Command `uvicorn main:app --host 0.0.0.0 --port $PORT` (this is automatically tracked inside the root `Procfile`).
- Add your `VIRLO_API_KEY` to the environment variables on the hosting platform.
