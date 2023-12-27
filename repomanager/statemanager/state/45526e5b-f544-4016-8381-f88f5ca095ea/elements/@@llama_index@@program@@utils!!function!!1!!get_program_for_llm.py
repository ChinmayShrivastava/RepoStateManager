def get_program_for_llm(
    output_cls: BaseModel,
    prompt: PromptTemplate,
    llm: LLM,
    pydantic_program_mode: PydanticProgramMode = PydanticProgramMode.DEFAULT,
    **kwargs: Any,
) -> BasePydanticProgram:
    """Get a program based on the compatible LLM."""
    if pydantic_program_mode == PydanticProgramMode.DEFAULT:
        # in default mode, we try to use the OpenAI program if available else
        # we fall back to the LLM program
        try:
            from llama_index.program.openai_program import OpenAIPydanticProgram

            return OpenAIPydanticProgram.from_defaults(
                output_cls=output_cls,
                llm=llm,
                prompt=prompt,
                **kwargs,
            )
        except ValueError:
            from llama_index.program.llm_program import LLMTextCompletionProgram

            return LLMTextCompletionProgram.from_defaults(
                output_parser=PydanticOutputParser(output_cls=output_cls),
                llm=llm,
                prompt=prompt,
                **kwargs,
            )
    elif pydantic_program_mode == PydanticProgramMode.OPENAI:
        from llama_index.program.openai_program import OpenAIPydanticProgram

        return OpenAIPydanticProgram.from_defaults(
            output_cls=output_cls,
            llm=llm,
            prompt=prompt,
            **kwargs,
        )
    elif pydantic_program_mode == PydanticProgramMode.LLM:
        from llama_index.program.llm_program import LLMTextCompletionProgram

        return LLMTextCompletionProgram.from_defaults(
            output_parser=PydanticOutputParser(output_cls=output_cls),
            llm=llm,
            prompt=prompt,
            **kwargs,
        )
    elif pydantic_program_mode == PydanticProgramMode.LM_FORMAT_ENFORCER:
        from llama_index.program.lmformatenforcer_program import (
            LMFormatEnforcerPydanticProgram,
        )

        return LMFormatEnforcerPydanticProgram.from_defaults(
            output_cls=output_cls,
            llm=llm,
            prompt=prompt,
            **kwargs,
        )
    else:
        raise ValueError(f"Unsupported pydantic program mode: {pydantic_program_mode}")
