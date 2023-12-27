class BaseAgentChatFormatter(BaseModel):
    """Base chat formatter."""

    class Config:
        arbitrary_types_allowed = True

    @abstractmethod
    def format(
        self,
        tools: Sequence[BaseTool],
        chat_history: List[ChatMessage],
        current_reasoning: Optional[List[BaseReasoningStep]] = None,
    ) -> List[ChatMessage]:
        """Format chat history into list of ChatMessage."""
