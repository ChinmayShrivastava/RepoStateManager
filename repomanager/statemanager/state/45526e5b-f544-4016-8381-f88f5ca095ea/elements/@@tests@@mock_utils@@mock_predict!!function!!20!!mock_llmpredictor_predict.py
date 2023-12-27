def mock_llmpredictor_predict(prompt: BasePromptTemplate, **prompt_args: Any) -> str:
    """Mock predict method of LLMPredictor.

    Depending on the prompt, return response.

    """
    full_prompt_args = {
        **prompt.kwargs,
        **prompt_args,
    }
    prompt_type = prompt.metadata["prompt_type"]
    if prompt_type == PromptType.SUMMARY:
        response = _mock_summary_predict(full_prompt_args)
    elif prompt_type == PromptType.TREE_INSERT:
        response = _mock_insert_predict()
    elif prompt_type == PromptType.TREE_SELECT:
        response = _mock_query_select()
    elif prompt_type == PromptType.REFINE:
        response = _mock_refine(full_prompt_args)
    elif prompt_type == PromptType.QUESTION_ANSWER:
        response = _mock_answer(full_prompt_args)
    elif prompt_type == PromptType.KEYWORD_EXTRACT:
        response = _mock_keyword_extract(full_prompt_args)
    elif prompt_type == PromptType.QUERY_KEYWORD_EXTRACT:
        response = _mock_query_keyword_extract(full_prompt_args)
    elif prompt_type == PromptType.SCHEMA_EXTRACT:
        response = _mock_schema_extract(full_prompt_args)
    elif prompt_type == PromptType.TEXT_TO_SQL:
        response = _mock_text_to_sql(full_prompt_args)
    elif prompt_type == PromptType.KNOWLEDGE_TRIPLET_EXTRACT:
        response = _mock_kg_triplet_extract(full_prompt_args)
    elif prompt_type == PromptType.SIMPLE_INPUT:
        response = _mock_input(full_prompt_args)
    elif prompt_type == PromptType.SINGLE_SELECT:
        response = _mock_single_select()
    elif prompt_type == PromptType.MULTI_SELECT:
        response = _mock_multi_select(full_prompt_args)
    elif prompt_type == PromptType.SUB_QUESTION:
        response = _mock_sub_questions()
    elif prompt_type == PromptType.PANDAS:
        response = _mock_pandas(full_prompt_args)
    elif prompt_type == PromptType.SQL_RESPONSE_SYNTHESIS:
        response = _mock_sql_response_synthesis(full_prompt_args)
    elif prompt_type == PromptType.SQL_RESPONSE_SYNTHESIS_V2:
        response = _mock_sql_response_synthesis_v2(full_prompt_args)
    elif prompt_type == PromptType.DECOMPOSE:
        response = _mock_decompose_query(full_prompt_args)
    elif prompt_type == PromptType.CHOICE_SELECT:
        response = _mock_choice_select(full_prompt_args)
    elif prompt_type == PromptType.CONVERSATION:
        response = _mock_conversation(full_prompt_args)
    else:
        response = str(full_prompt_args)

    return response
