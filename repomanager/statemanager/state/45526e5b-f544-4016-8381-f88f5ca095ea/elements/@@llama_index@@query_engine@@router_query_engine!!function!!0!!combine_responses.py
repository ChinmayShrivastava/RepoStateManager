def combine_responses(
    summarizer: TreeSummarize, responses: List[RESPONSE_TYPE], query_bundle: QueryBundle
) -> RESPONSE_TYPE:
    """Combine multiple response from sub-engines."""
    logger.info("Combining responses from multiple query engines.")

    response_strs = []
    source_nodes = []
    for response in responses:
        if isinstance(response, (StreamingResponse, PydanticResponse)):
            response_obj = response.get_response()
        else:
            response_obj = response
        source_nodes.extend(response_obj.source_nodes)
        response_strs.append(str(response))

    summary = summarizer.get_response(query_bundle.query_str, response_strs)

    if isinstance(summary, str):
        return Response(response=summary, source_nodes=source_nodes)
    elif isinstance(summary, BaseModel):
        return PydanticResponse(response=summary, source_nodes=source_nodes)
    else:
        return StreamingResponse(response_gen=summary, source_nodes=source_nodes)
