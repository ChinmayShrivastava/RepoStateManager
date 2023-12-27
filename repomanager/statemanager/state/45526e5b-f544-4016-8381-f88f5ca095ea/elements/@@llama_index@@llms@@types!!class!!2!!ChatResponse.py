class ChatResponse(BaseModel):
    """Chat response."""

    message: ChatMessage
    raw: Optional[dict] = None
    delta: Optional[str] = None
    additional_kwargs: dict = Field(default_factory=dict)

    def __str__(self) -> str:
        return str(self.message)
