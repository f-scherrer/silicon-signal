from pydantic import BaseModel, Field
from typing import Literal, Optional
from datetime import datetime

class Bar(BaseModel):
    ticker: str
    ts: datetime
    open: float; high: float; low: float; close: float
    volume: float
    timeframe: Literal["1d","1h","W"]

class FeatureFrameMeta(BaseModel):
    ticker: str
    freq: Literal["D","W","M"]
    source: str
    version: str = "0.1.0"

class SentimentDoc(BaseModel):
    doc_id: str
    ts: datetime
    ticker: Optional[str] = None
    provider: Literal["news","social"]
    score: float
    meta: dict = Field(default_factory=dict)
