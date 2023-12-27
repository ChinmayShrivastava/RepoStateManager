def override_predict(self: Any, prompt: BasePromptTemplate, **prompt_args: Any) -> str:
    return prompt.format(**prompt_args)
