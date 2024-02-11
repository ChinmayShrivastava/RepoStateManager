from pydantic import BaseModel
from typing import List

class SimilarityResult(BaseModel):
    similarity: float
    document: str
    id: int
    metadata: dict

class SimilarityResults(BaseModel):
    results: List[SimilarityResult]