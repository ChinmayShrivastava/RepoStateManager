def generate_answer(
    *,
    prompt: str,
    passages: List[str],
    answer_style: int = genai.GenerateAnswerRequest.AnswerStyle.ABSTRACTIVE,
    safety_settings: List[genai.SafetySetting] = [],
    temperature: Optional[float] = None,
    client: genai.GenerativeServiceClient,
) -> GroundedAnswer:
    # TODO: Consider passing in the corpus ID instead of the actual
    # passages.
    response = client.generate_answer(
        genai.GenerateAnswerRequest(
            contents=[
                genai.Content(parts=[genai.Part(text=prompt)]),
            ],
            model=_DEFAULT_GENERATE_SERVICE_MODEL,
            answer_style=answer_style,
            safety_settings=safety_settings,
            temperature=temperature,
            inline_passages=genai.GroundingPassages(
                passages=[
                    genai.GroundingPassage(
                        # IDs here takes alphanumeric only. No dashes allowed.
                        id=str(index),
                        content=genai.Content(parts=[genai.Part(text=chunk)]),
                    )
                    for index, chunk in enumerate(passages)
                ]
            ),
        )
    )

    if response.answer.finish_reason != genai.Candidate.FinishReason.STOP:
        raise GenerateAnswerError(
            finish_reason=response.answer.finish_reason,
            finish_message=response.answer.finish_message,
            safety_ratings=response.answer.safety_ratings,
        )

    assert len(response.answer.content.parts) == 1
    return GroundedAnswer(
        answer=response.answer.content.parts[0].text,
        attributed_passages=[
            Passage(
                text=passage.content.parts[0].text,
                id=passage.source_id.grounding_passage.passage_id,
            )
            for passage in response.answer.grounding_attributions
            if len(passage.content.parts) > 0
        ],
        answerable_probability=response.answerable_probability,
    )
