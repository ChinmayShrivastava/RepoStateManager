def _validate_prompt(response_synthesis_prompt: BasePromptTemplate) -> None:
    """Validate prompt."""
    if (
        response_synthesis_prompt.template_vars
        != DEFAULT_RESPONSE_SYNTHESIS_PROMPT_V2.template_vars
    ):
        raise ValueError(
            "response_synthesis_prompt must have the following template variables: "
            "query_str, sql_query, context_str"
        )
