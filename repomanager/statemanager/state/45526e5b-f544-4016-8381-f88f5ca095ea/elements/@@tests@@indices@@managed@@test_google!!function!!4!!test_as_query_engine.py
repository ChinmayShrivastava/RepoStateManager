def test_as_query_engine(
    mock_get_corpus: MagicMock,
    mock_generate_answer: MagicMock,
    mock_query_corpus: MagicMock,
) -> None:
    # Arrange
    mock_get_corpus.return_value = genai.Corpus(name="corpora/123")
    mock_query_corpus.return_value = genai.QueryCorpusResponse(
        relevant_chunks=[
            genai.RelevantChunk(
                chunk=genai.Chunk(
                    name="corpora/123/documents/456/chunks/789",
                    data=genai.ChunkData(string_value="It's 42"),
                ),
                chunk_relevance_score=0.9,
            )
        ]
    )
    mock_generate_answer.return_value = genai.GenerateAnswerResponse(
        answer=genai.Candidate(
            content=genai.Content(parts=[genai.Part(text="42")]),
            grounding_attributions=[
                genai.GroundingAttribution(
                    content=genai.Content(
                        parts=[genai.Part(text="Meaning of life is 42")]
                    ),
                    source_id=genai.AttributionSourceId(
                        grounding_passage=genai.AttributionSourceId.GroundingPassageId(
                            passage_id="corpora/123/documents/456/chunks/777",
                            part_index=0,
                        )
                    ),
                ),
                genai.GroundingAttribution(
                    content=genai.Content(parts=[genai.Part(text="Or maybe not")]),
                    source_id=genai.AttributionSourceId(
                        grounding_passage=genai.AttributionSourceId.GroundingPassageId(
                            passage_id="corpora/123/documents/456/chunks/888",
                            part_index=0,
                        )
                    ),
                ),
            ],
            finish_reason=genai.Candidate.FinishReason.STOP,
        ),
        answerable_probability=0.9,
    )

    # Act
    index = GoogleIndex.from_corpus(corpus_id="123")
    query_engine = index.as_query_engine(
        answer_style=genai.GenerateAnswerRequest.AnswerStyle.EXTRACTIVE
    )
    response = query_engine.query("What is the meaning of life?")

    # Assert
    assert mock_query_corpus.call_count == 1
    query_corpus_request = mock_query_corpus.call_args.args[0]
    assert query_corpus_request.name == "corpora/123"
    assert query_corpus_request.query == "What is the meaning of life?"

    assert isinstance(response, Response)

    assert response.response == "42"

    assert mock_generate_answer.call_count == 1
    generate_answer_request = mock_generate_answer.call_args.args[0]
    assert (
        generate_answer_request.contents[0].parts[0].text
        == "What is the meaning of life?"
    )
    assert (
        generate_answer_request.answer_style
        == genai.GenerateAnswerRequest.AnswerStyle.EXTRACTIVE
    )

    passages = generate_answer_request.inline_passages.passages
    assert len(passages) == 1
    passage = passages[0]
    assert passage.content.parts[0].text == "It's 42"
