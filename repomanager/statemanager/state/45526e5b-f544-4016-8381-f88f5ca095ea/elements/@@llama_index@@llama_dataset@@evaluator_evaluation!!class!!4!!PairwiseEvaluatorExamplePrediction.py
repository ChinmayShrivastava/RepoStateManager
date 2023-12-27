class PairwiseEvaluatorExamplePrediction(BaseLlamaExamplePrediction):
    """Pairwise evaluation example prediction class.

    Args:
        feedback (Optional[str]): The evaluator's feedback.
        score (Optional[float]): The evaluator's score.
        evaluation_source (EvaluationSource): If the evaluation came from original order or flipped; or inconclusive.
    """

    feedback: str = Field(
        default_factory=str,
        description="The generated (predicted) response that can be compared to a reference (ground-truth) answer.",
    )
    score: Optional[float] = Field(
        default=None,
        description="The generated (predicted) response that can be compared to a reference (ground-truth) answer.",
    )
    evaluation_source: Optional[EvaluationSource] = Field(
        default=None,
        description=(
            "Whether the evaluation comes from original, or flipped ordering. Can also be neither here indicating inconclusive judgement."
        ),
    )
    invalid_prediction: bool = Field(
        default=False, description="Whether or not the prediction is a valid one."
    )
    invalid_reason: Optional[str] = Field(
        default=None, description="Reason as to why prediction is invalid."
    )

    @property
    def class_name(self) -> str:
        """Data example class name."""
        return "PairwiseEvaluatorExamplePrediction"
