class VellumCompiledPrompt:
    """Represents a compiled prompt from Vellum with all string substitutions,
    templating, etc. applied.
    """

    text: str
    num_tokens: int
