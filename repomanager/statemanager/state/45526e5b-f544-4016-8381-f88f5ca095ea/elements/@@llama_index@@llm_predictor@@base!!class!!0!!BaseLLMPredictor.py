class BaseLLMPredictor(BaseComponent, ABC):
    """Base LLM Predictor."""

    def dict(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().dict(**kwargs)
        data["llm"] = self.llm.to_dict()
        return data

    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        data = super().to_dict(**kwargs)
        data["llm"] = self.llm.to_dict()
        return data

    @property
    @abstractmethod
    def llm(self) -> LLM:
        """Get LLM."""

    @property
    @abstractmethod
    def callback_manager(self) -> CallbackManager:
        """Get callback manager."""

    @property
    @abstractmethod
    def metadata(self) -> LLMMetadata:
        """Get LLM metadata."""

    @abstractmethod
    def predict(self, prompt: BasePromptTemplate, **prompt_args: Any) -> str:
        """Predict the answer to a query."""

    @abstractmethod
    def stream(self, prompt: BasePromptTemplate, **prompt_args: Any) -> TokenGen:
        """Stream the answer to a query."""

    @abstractmethod
    async def apredict(self, prompt: BasePromptTemplate, **prompt_args: Any) -> str:
        """Async predict the answer to a query."""

    @abstractmethod
    async def astream(
        self, prompt: BasePromptTemplate, **prompt_args: Any
    ) -> TokenAsyncGen:
        """Async predict the answer to a query."""
