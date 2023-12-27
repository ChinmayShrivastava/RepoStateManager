class CohereEmbedding(BaseEmbedding):
    """CohereEmbedding uses the Cohere API to generate embeddings for text."""

    # Instance variables initialized via Pydantic's mechanism
    cohere_client: Any = Field(description="CohereAI client")
    truncate: str = Field(description="Truncation type - START/ END/ NONE")
    input_type: Optional[str] = Field(description="Model Input type")

    def __init__(
        self,
        cohere_api_key: Optional[str] = None,
        model_name: str = "embed-english-v2.0",
        truncate: str = "END",
        input_type: Optional[str] = None,
        embed_batch_size: int = DEFAULT_EMBED_BATCH_SIZE,
        callback_manager: Optional[CallbackManager] = None,
    ):
        """
        A class representation for generating embeddings using the Cohere API.

        Args:
            cohere_client (Any): An instance of the Cohere client, which is used to communicate with the Cohere API.
            truncate (str): A string indicating the truncation strategy to be applied to input text. Possible values
                        are 'START', 'END', or 'NONE'.
            input_type (Optional[str]): An optional string that specifies the type of input provided to the model.
                                    This is model-dependent and could be one of the following: 'search_query',
                                    'search_document', 'classification', or 'clustering'.
            model_name (str): The name of the model to be used for generating embeddings. The class ensures that
                          this model is supported and that the input type provided is compatible with the model.
        """
        # Attempt to import cohere. If it fails, raise an informative ImportError.
        try:
            import cohere
        except ImportError:
            raise ImportError(
                "CohereEmbedding requires the 'cohere' package to be installed.\n"
                "Please install it with `pip install cohere`."
            )
        # Validate model_name and input_type
        if (model_name, input_type) not in VALID_MODEL_INPUT_TYPES:
            raise ValueError(
                f"{(model_name, input_type)} is not valid for model '{model_name}'"
            )

        if truncate not in VALID_TRUNCATE_OPTIONS:
            raise ValueError(f"truncate must be one of {VALID_TRUNCATE_OPTIONS}")

        super().__init__(
            cohere_client=cohere.Client(cohere_api_key),
            cohere_api_key=cohere_api_key,
            model_name=model_name,
            truncate=truncate,
            input_type=input_type,
            embed_batch_size=embed_batch_size,
            callback_manager=callback_manager,
        )

    @classmethod
    def class_name(cls) -> str:
        return "CohereEmbedding"

    def _embed(self, texts: List[str]) -> List[List[float]]:
        """Embed sentences using Cohere."""
        if self.input_type:
            result = self.cohere_client.embed(
                texts=texts,
                input_type=self.input_type,
                model=self.model_name,
                truncate=self.truncate,
            ).embeddings
        else:
            result = self.cohere_client.embed(
                texts=texts, model=self.model_name, truncate=self.truncate
            ).embeddings
        return [list(map(float, e)) for e in result]

    def _get_query_embedding(self, query: str) -> List[float]:
        """Get query embedding."""
        return self._embed([query])[0]

    async def _aget_query_embedding(self, query: str) -> List[float]:
        """Get query embedding async."""
        return self._get_query_embedding(query)

    def _get_text_embedding(self, text: str) -> List[float]:
        """Get text embedding."""
        return self._embed([text])[0]

    async def _aget_text_embedding(self, text: str) -> List[float]:
        """Get text embedding async."""
        return self._get_text_embedding(text)

    def _get_text_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get text embeddings."""
        return self._embed(texts)
