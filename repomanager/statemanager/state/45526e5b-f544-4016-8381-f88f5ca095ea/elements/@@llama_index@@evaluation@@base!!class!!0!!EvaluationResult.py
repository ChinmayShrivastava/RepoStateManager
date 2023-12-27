class EvaluationResult(BaseModel):
    """Evaluation result.

    Output of an BaseEvaluator.
    """

    query: Optional[str] = Field(None, description="Query string")
    contexts: Optional[Sequence[str]] = Field(None, description="Context strings")
    response: Optional[str] = Field(None, description="Response string")
    passing: Optional[bool] = Field(
        None, description="Binary evaluation result (passing or not)"
    )
    feedback: Optional[str] = Field(
        None, description="Feedback or reasoning for the response"
    )
    score: Optional[float] = Field(None, description="Score for the response")
    pairwise_source: Optional[str] = Field(
        None,
        description=(
            "Used only for pairwise and specifies whether it is from original order of"
            " presented answers or flipped order"
        ),
    )
    invalid_result: bool = Field(
        default=False, description="Whether the evaluation result is an invalid one."
    )
    invalid_reason: Optional[str] = Field(
        default=None, description="Reason for invalid evaluation."
    )
