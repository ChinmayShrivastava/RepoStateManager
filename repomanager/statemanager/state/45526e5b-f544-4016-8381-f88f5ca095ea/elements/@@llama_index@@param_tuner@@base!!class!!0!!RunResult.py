class RunResult(BaseModel):
    """Run result."""

    score: float
    params: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata.")
