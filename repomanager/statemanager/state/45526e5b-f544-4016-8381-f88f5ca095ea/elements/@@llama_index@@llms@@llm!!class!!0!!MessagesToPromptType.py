class MessagesToPromptType(Protocol):
    def __call__(self, messages: Sequence[ChatMessage]) -> str:
        pass
