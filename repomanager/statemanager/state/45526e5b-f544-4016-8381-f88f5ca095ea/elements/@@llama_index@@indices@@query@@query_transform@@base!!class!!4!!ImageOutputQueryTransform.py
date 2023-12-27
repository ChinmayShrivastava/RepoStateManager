class ImageOutputQueryTransform(BaseQueryTransform):
    """Image output query transform.

    Adds instructions for formatting image output.
    By default, this prompts the LLM to format image output as an HTML <img> tag,
    which can be displayed nicely in jupyter notebook.
    """

    def __init__(
        self,
        width: int = 400,
        query_prompt: Optional[ImageOutputQueryTransformPrompt] = None,
    ) -> None:
        """Init ImageOutputQueryTransform.

        Args:
            width (int): desired image display width in pixels
            query_prompt (ImageOutputQueryTransformPrompt): custom prompt for
                augmenting query with image output instructions.
        """
        self._width = width
        self._query_prompt = query_prompt or DEFAULT_IMAGE_OUTPUT_PROMPT

    def _get_prompts(self) -> PromptDictType:
        """Get prompts."""
        return {"query_prompt": self._query_prompt}

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        if "query_prompt" in prompts:
            self._query_prompt = prompts["query_prompt"]

    def _run(self, query_bundle: QueryBundle, metadata: Dict) -> QueryBundle:
        """Run query transform."""
        del metadata  # Unused
        new_query_str = self._query_prompt.format(
            query_str=query_bundle.query_str, image_width=self._width
        )
        return dataclasses.replace(query_bundle, query_str=new_query_str)
