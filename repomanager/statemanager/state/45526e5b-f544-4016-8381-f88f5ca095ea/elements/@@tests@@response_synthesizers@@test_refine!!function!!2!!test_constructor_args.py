def test_constructor_args(mock_refine_service_context: ServiceContext) -> None:
    with pytest.raises(ValueError):
        # can't construct refine with both streaming and answer filtering
        Refine(
            service_context=mock_refine_service_context,
            streaming=True,
            structured_answer_filtering=True,
        )
    with pytest.raises(ValueError):
        # can't construct refine with a program factory but not answer filtering
        Refine(
            service_context=mock_refine_service_context,
            program_factory=lambda _: MockRefineProgram({}),
            structured_answer_filtering=False,
        )
