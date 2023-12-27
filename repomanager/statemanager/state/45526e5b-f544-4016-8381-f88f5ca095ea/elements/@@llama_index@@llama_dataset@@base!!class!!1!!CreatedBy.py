class CreatedBy(BaseModel):
    model_name: Optional[str] = Field(
        default_factory=str, description="When CreatedByType.AI, specify model name."
    )
    type: CreatedByType

    def __str__(self) -> str:
        if self.type == "ai":
            return f"{self.type!s} ({self.model_name})"
        else:
            return str(self.type)
