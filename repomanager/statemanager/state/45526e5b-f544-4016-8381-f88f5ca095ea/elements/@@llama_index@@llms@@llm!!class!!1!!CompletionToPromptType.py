class CompletionToPromptType(Protocol):
    def __call__(self, prompt: str) -> str:
        pass
