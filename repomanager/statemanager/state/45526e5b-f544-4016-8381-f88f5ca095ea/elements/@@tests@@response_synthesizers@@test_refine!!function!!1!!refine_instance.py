def refine_instance(mock_refine_service_context: ServiceContext) -> Refine:
    return Refine(
        service_context=mock_refine_service_context,
        streaming=False,
        verbose=True,
        structured_answer_filtering=True,
    )
