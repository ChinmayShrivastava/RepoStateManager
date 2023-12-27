def delete_chunk(
    *,
    corpus_id: str,
    document_id: str,
    chunk_id: str,
    client: genai.RetrieverServiceClient,
) -> None:
    client.delete_chunk(
        genai.DeleteChunkRequest(
            name=str(
                EntityName(
                    corpus_id=corpus_id, document_id=document_id, chunk_id=chunk_id
                )
            )
        )
    )
