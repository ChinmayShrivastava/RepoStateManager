class SynthesizedResponse(BaseModel):
    """Response of `GoogleTextSynthesizer.get_response`."""

    answer: str
    """The grounded response to the user's question."""

    attributed_passages: List[str]
    """The list of passages the AQA model used for its response."""

    answerable_probability: float
    """The model's estimate of the probability that its answer is correct and grounded in the input passages."""
