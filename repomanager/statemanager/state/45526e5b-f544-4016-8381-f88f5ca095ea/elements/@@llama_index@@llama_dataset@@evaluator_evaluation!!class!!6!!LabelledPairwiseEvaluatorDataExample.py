class LabelledPairwiseEvaluatorDataExample(LabelledEvaluatorDataExample):
    """Labelled pairwise evaluation data example class."""

    second_answer: str = Field(
        default_factory=str,
        description="The second answer to the example that is to be evaluated along versus `answer`.",
    )
    second_answer_by: Optional[CreatedBy] = Field(
        default=None, description="What generated the second answer."
    )

    @property
    def class_name(self) -> str:
        """Data example class name."""
        return "LabelledPairwiseEvaluatorDataExample"
