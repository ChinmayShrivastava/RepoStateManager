class RetrievalEvalResult(BaseModel):
    """Retrieval eval result.

    NOTE: this abstraction might change in the future.

    Attributes:
        query (str): Query string
        expected_ids (List[str]): Expected ids
        retrieved_ids (List[str]): Retrieved ids
        metric_dict (Dict[str, BaseRetrievalMetric]): \
            Metric dictionary for the evaluation

    """

    class Config:
        arbitrary_types_allowed = True

    query: str = Field(..., description="Query string")
    expected_ids: List[str] = Field(..., description="Expected ids")
    expected_texts: Optional[List[str]] = Field(
        default=None,
        description="Expected texts associated with nodes provided in `expected_ids`",
    )
    retrieved_ids: List[str] = Field(..., description="Retrieved ids")
    retrieved_texts: List[str] = Field(..., description="Retrieved texts")
    mode: "RetrievalEvalMode" = Field(
        default=RetrievalEvalMode.TEXT, description="text or image"
    )
    metric_dict: Dict[str, RetrievalMetricResult] = Field(
        ..., description="Metric dictionary for the evaluation"
    )

    @property
    def metric_vals_dict(self) -> Dict[str, float]:
        """Dictionary of metric values."""
        return {k: v.score for k, v in self.metric_dict.items()}

    def __str__(self) -> str:
        """String representation."""
        return f"Query: {self.query}\n" f"Metrics: {self.metric_vals_dict!s}\n"
