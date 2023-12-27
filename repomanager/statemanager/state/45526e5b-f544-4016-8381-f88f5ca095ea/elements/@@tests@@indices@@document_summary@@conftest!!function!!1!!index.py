def index(
    docs: List[Document], mock_service_context: ServiceContext
) -> DocumentSummaryIndex:
    response_synthesizer = get_response_synthesizer(
        text_qa_template=MOCK_TEXT_QA_PROMPT,
        refine_template=MOCK_REFINE_PROMPT,
        callback_manager=mock_service_context.callback_manager,
    )
    return DocumentSummaryIndex.from_documents(
        docs,
        service_context=mock_service_context,
        response_synthesizer=response_synthesizer,
        summary_query="summary_query",
    )
