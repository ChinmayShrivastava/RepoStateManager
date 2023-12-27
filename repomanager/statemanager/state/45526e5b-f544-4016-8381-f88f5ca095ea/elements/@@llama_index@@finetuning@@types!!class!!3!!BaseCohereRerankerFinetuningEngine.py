class BaseCohereRerankerFinetuningEngine(ABC):
    """Base Cohere Reranker Finetuning Engine."""

    @abstractmethod
    def finetune(self) -> None:
        """Goes off and does stuff."""

    @abstractmethod
    def get_finetuned_model(self, top_n: int = 5) -> CohereRerank:
        """Gets finetuned model."""
