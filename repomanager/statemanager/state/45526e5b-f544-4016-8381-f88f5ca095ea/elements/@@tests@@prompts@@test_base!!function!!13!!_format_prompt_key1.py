    def _format_prompt_key1(**kwargs: Any) -> str:
        """Given kwargs, output formatted variable."""
        return f"{kwargs['prompt_key1']}-{kwargs['prompt_key2']}"
