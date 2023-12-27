def test_get_response(mock_generate_answer: MagicMock) -> None:
    # Arrange
    mock_generate_answer.return_value = genai.GenerateAnswerResponse(
        answer=genai.Candidate(
            content=genai.Content(parts=[genai.Part(text="42")]),
            grounding_attributions=[
                genai.GroundingAttribution(
                    content=genai.Content(
                        parts=[genai.Part(text="Meaning of life is 42.")]
                    ),
                    source_id=genai.AttributionSourceId(
                        grounding_passage=genai.AttributionSourceId.GroundingPassageId(
                            passage_id="corpora/123/documents/456/chunks/789",
                            part_index=0,
                        )
                    ),
                ),
            ],
            finish_reason=genai.Candidate.FinishReason.STOP,
        ),
        answerable_probability=0.7,
    )

    # Act
    synthesizer = GoogleTextSynthesizer.from_defaults(
        temperature=0.5,
        answer_style=genai.GenerateAnswerRequest.AnswerStyle.ABSTRACTIVE,
        safety_setting=[
            genai.SafetySetting(
                category=genai.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=genai.SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            )
        ],
    )
    response = synthesizer.get_response(
        query_str="What is the meaning of life?",
        text_chunks=[
            "It's 42",
        ],
    )

    # Assert
    assert response.answer == "42"
    assert response.attributed_passages == ["Meaning of life is 42."]
    assert response.answerable_probability == pytest.approx(0.7)

    assert mock_generate_answer.call_count == 1
    request = mock_generate_answer.call_args.args[0]
    assert request.contents[0].parts[0].text == "What is the meaning of life?"

    assert request.answer_style == genai.GenerateAnswerRequest.AnswerStyle.ABSTRACTIVE

    assert len(request.safety_settings) == 1
    assert (
        request.safety_settings[0].category
        == genai.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT
    )
    assert (
        request.safety_settings[0].threshold
        == genai.SafetySetting.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE
    )

    assert request.temperature == 0.5

    passages = request.inline_passages.passages
    assert len(passages) == 1
    passage = passages[0]
    assert passage.content.parts[0].text == "It's 42"
