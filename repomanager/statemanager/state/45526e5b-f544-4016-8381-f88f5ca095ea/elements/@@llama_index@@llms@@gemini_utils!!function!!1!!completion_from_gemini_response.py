def completion_from_gemini_response(
    response: Union[
        "genai.types.GenerateContentResponse",
        "genai.types.AsyncGenerateContentResponse",
    ],
) -> CompletionResponse:
    top_candidate = response.candidates[0]
    _error_if_finished_early(top_candidate)

    raw = {
        **(type(top_candidate).to_dict(top_candidate)),
        **(type(response.prompt_feedback).to_dict(response.prompt_feedback)),
    }
    return CompletionResponse(text=response.text, raw=raw)
