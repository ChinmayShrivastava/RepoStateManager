def test_synthesize(mock_generate_answer: MagicMock) -> None:
    # Arrange
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
    synthesizer = GoogleTextSynthesizer.from_defaults()
    response = synthesizer.synthesize(
        query="What is the meaning of life?",
        nodes=[
            NodeWithScore(
                node=TextNode(text="It's 42"),
                score=0.5,
            ),
        ],
        additional_source_nodes=[
            NodeWithScore(
                node=TextNode(text="Additional node"),
                score=0.4,
            ),
        ],
    )

    # Assert
    assert response.response == "42"
    assert len(response.source_nodes) == 4

    first_attributed_source = response.source_nodes[0]
    assert first_attributed_source.node.text == "Meaning of life is 42"
    assert first_attributed_source.score is None

    second_attributed_source = response.source_nodes[1]
    assert second_attributed_source.node.text == "Or maybe not"
    assert second_attributed_source.score is None

    first_input_source = response.source_nodes[2]
    assert first_input_source.node.text == "It's 42"
    assert first_input_source.score == pytest.approx(0.5)

    first_additional_source = response.source_nodes[3]
    assert first_additional_source.node.text == "Additional node"
    assert first_additional_source.score == pytest.approx(0.4)

    assert response.metadata is not None
    assert response.metadata.get("answerable_probability", None) == pytest.approx(0.9)
