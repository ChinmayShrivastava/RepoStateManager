class GenerateAnswerError(Exception):
    finish_reason: genai.Candidate.FinishReason
    finish_message: str
    safety_ratings: MutableSequence[genai.SafetyRating]

    def __str__(self) -> str:
        return (
            f"finish_reason: {self.finish_reason.name} "
            f"finish_message: {self.finish_message} "
            f"safety ratings: {self.safety_ratings}"
        )
