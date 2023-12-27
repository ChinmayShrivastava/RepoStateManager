    def fake_stream() -> Iterator[vellum.GenerateStreamResponse]:
        yield vellum.GenerateStreamResponse(
            delta=vellum.GenerateStreamResult(
                request_index=0,
                data=vellum.GenerateStreamResultData(
                    completion_index=0,
                    completion=vellum.EnrichedNormalizedCompletion(
                        id="123", text="Hello,", model_version_id="abc"
                    ),
                ),
                error=None,
            )
        )
        yield vellum.GenerateStreamResponse(
            delta=vellum.GenerateStreamResult(
                request_index=0,
                data=vellum.GenerateStreamResultData(
                    completion_index=0,
                    completion=vellum.EnrichedNormalizedCompletion(
                        id="456", text=" world!", model_version_id="abc"
                    ),
                ),
                error=None,
            )
        )
