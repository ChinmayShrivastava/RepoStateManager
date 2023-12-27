class BaseCrossEncoderFinetuningEngine(ABC):
    """Base Cross Encoder Finetuning Engine."""

    @abstractmethod
    def finetune(self) -> None:
        """Goes off and does stuff."""

    @abstractmethod
    def get_finetuned_model(
        self, model_name: str, top_n: int = 3
    ) -> SentenceTransformerRerank:
        """Gets fine-tuned Cross-Encoder model as re-ranker."""
