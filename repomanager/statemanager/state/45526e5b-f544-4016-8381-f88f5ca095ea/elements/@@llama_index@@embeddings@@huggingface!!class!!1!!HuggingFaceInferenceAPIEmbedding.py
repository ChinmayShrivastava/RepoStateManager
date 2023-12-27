class HuggingFaceInferenceAPIEmbedding(HuggingFaceInferenceAPI, BaseEmbedding):  # type: ignore[misc]
    """
    Wrapper on the Hugging Face's Inference API for embeddings.

    Overview of the design:
    - Uses the feature extraction task: https://huggingface.co/tasks/feature-extraction
    """

    pooling: Optional[Pooling] = Field(
        default=Pooling.CLS,
        description=(
            "Optional pooling technique to use with embeddings capability, if"
            " the model's raw output needs pooling."
        ),
    )
    query_instruction: Optional[str] = Field(
        default=None,
        description=(
            "Instruction to prepend during query embedding."
            " Use of None means infer the instruction based on the model."
            " Use of empty string will defeat instruction prepending entirely."
        ),
    )
    text_instruction: Optional[str] = Field(
        default=None,
        description=(
            "Instruction to prepend during text embedding."
            " Use of None means infer the instruction based on the model."
            " Use of empty string will defeat instruction prepending entirely."
        ),
    )

    @classmethod
    def class_name(cls) -> str:
        return "HuggingFaceInferenceAPIEmbedding"

    async def _async_embed_single(self, text: str) -> Embedding:
        embedding = await self._async_client.feature_extraction(text)
        if len(embedding.shape) == 1:
            return embedding.tolist()
        embedding = embedding.squeeze(axis=0)
        if len(embedding.shape) == 1:  # Some models pool internally
            return embedding.tolist()
        try:
            return self.pooling(embedding).tolist()  # type: ignore[misc]
        except TypeError as exc:
            raise ValueError(
                f"Pooling is required for {self.model_name} because it returned"
                " a > 1-D value, please specify pooling as not None."
            ) from exc

    async def _async_embed_bulk(self, texts: Sequence[str]) -> List[Embedding]:
        """
        Embed a sequence of text, in parallel and asynchronously.

        NOTE: this uses an externally created asyncio event loop.
        """
        tasks = [self._async_embed_single(text) for text in texts]
        return await asyncio.gather(*tasks)

    def _get_query_embedding(self, query: str) -> Embedding:
        """
        Embed the input query synchronously.

        NOTE: a new asyncio event loop is created internally for this.
        """
        return asyncio.run(self._aget_query_embedding(query))

    def _get_text_embedding(self, text: str) -> Embedding:
        """
        Embed the text query synchronously.

        NOTE: a new asyncio event loop is created internally for this.
        """
        return asyncio.run(self._aget_text_embedding(text))

    def _get_text_embeddings(self, texts: List[str]) -> List[Embedding]:
        """
        Embed the input sequence of text synchronously and in parallel.

        NOTE: a new asyncio event loop is created internally for this.
        """
        loop = asyncio.new_event_loop()
        try:
            tasks = [
                loop.create_task(self._aget_text_embedding(text)) for text in texts
            ]
            loop.run_until_complete(asyncio.wait(tasks))
        finally:
            loop.close()
        return [task.result() for task in tasks]

    async def _aget_query_embedding(self, query: str) -> Embedding:
        return await self._async_embed_single(
            text=format_query(query, self.model_name, self.query_instruction)
        )

    async def _aget_text_embedding(self, text: str) -> Embedding:
        return await self._async_embed_single(
            text=format_text(text, self.model_name, self.text_instruction)
        )

    async def _aget_text_embeddings(self, texts: List[str]) -> List[Embedding]:
        return await self._async_embed_bulk(
            texts=[
                format_text(text, self.model_name, self.text_instruction)
                for text in texts
            ]
        )
