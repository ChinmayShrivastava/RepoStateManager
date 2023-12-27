class ObservationReasoningStep(BaseReasoningStep):
    """Observation reasoning step."""

    observation: str

    def get_content(self) -> str:
        """Get content."""
        return f"Observation: {self.observation}"

    @property
    def is_done(self) -> bool:
        """Is the reasoning step the last one."""
        return False
