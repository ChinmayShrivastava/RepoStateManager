class EvaluatorExamplePrediction(BaseLlamaExamplePrediction):
    """Evaluation example prediction class.

    Args:
        feedback (Optional[str]): The evaluator's feedback.
        score (Optional[float]): The evaluator's score.
    """

    feedback: str = Field(
        default_factory=str,
        description="The generated (predicted) response that can be compared to a reference (ground-truth) answer.",
    )
    score: Optional[float] = Field(
        default=None,
        description="The generated (predicted) response that can be compared to a reference (ground-truth) answer.",
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
        return "EvaluatorExamplePrediction"
