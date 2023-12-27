def _match(
    llm: OpenAI, question: str, reference_answer: str, hypothesis_answer: str
) -> bool:
    prompt = match_template.format(
        question=question,
        reference_answer=reference_answer,
        hypothesis_answer=hypothesis_answer,
    )
    response = llm.chat([ChatMessage(role=MessageRole.USER, content=prompt)])
    content = response.message.content or ""
    return "true" in content.lower()
