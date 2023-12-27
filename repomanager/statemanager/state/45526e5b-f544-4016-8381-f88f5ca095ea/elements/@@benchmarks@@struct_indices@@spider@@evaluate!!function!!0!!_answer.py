def _answer(
    llm: OpenAI, question: str, sql_query: str, sql_result: Optional[str]
) -> str:
    prompt = answer_template.format(
        question=question, sql_query=sql_query, sql_result=sql_result
    )
    response = llm.chat([ChatMessage(role=MessageRole.USER, content=prompt)])
    return response.message.content or ""
