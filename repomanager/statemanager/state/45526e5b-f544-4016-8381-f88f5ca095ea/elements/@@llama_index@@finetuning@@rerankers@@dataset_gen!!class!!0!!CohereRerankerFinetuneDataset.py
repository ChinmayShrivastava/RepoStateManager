class CohereRerankerFinetuneDataset(BaseModel):
    """Class for keeping track of CohereAI Reranker finetuning training/validation Dataset."""

    query: str
    relevant_passages: List[str]
    hard_negatives: Any

    def to_jsonl(self) -> str:
        """Convert the BaseModel instance to a JSONL string."""
        return self.json() + "\n"
