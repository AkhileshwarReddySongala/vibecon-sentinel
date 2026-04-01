from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import uuid

class VirloContentItem(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    source: str
    niche: str
    headline: str
    raw_content: str
    extracted_at: datetime = Field(default_factory=datetime.utcnow)
    url: Optional[str] = None

class FactSheet(BaseModel):
    article_id: str
    headline: str
    key_entities: List[str]
    timeline_events: List[str]
    core_claims: List[str]
    supporting_evidence: List[str]
    credibility_score: int = Field(ge=0, le=100)
    
class EditorialArticle(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    headline: str
    subheadline: str
    body_markdown: str
    niche: str
    published_at: datetime = Field(default_factory=datetime.utcnow)
    fact_sheet_ref: str
    sources_analyzed: int = 0
    overlapping_signals_merged: int = 0
    fact_sheet: Optional[FactSheet] = None
    virlo_enrichment_data: Optional[dict] = None
