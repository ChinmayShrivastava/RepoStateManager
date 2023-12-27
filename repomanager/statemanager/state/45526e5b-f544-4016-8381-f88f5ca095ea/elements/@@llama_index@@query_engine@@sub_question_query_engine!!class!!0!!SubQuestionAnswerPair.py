class SubQuestionAnswerPair(BaseModel):
    """
    Pair of the sub question and optionally its answer (if its been answered yet).
    """

    sub_q: SubQuestion
    answer: Optional[str] = None
    sources: List[NodeWithScore] = Field(default_factory=list)
