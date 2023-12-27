def batch_create_chunk(
    *,
    corpus_id: str,
    document_id: str,
    texts: List[str],
    metadatas: Optional[List[Dict[str, Any]]] = None,
    client: genai.RetrieverServiceClient,
) -> List[genai.Chunk]:
    if metadatas is None:
        metadatas = [{} for _ in texts]
    if len(texts) != len(metadatas):
        raise ValueError(
            f"metadatas's length {len(metadatas)} and texts's length {len(texts)} are mismatched"
        )

    doc_name = str(EntityName(corpus_id=corpus_id, document_id=document_id))

    created_chunks: List[genai.Chunk] = []

    batch_request = genai.BatchCreateChunksRequest(
        parent=doc_name,
        requests=[],
    )
    for text, metadata in zip(texts, metadatas):
        batch_request.requests.append(
            genai.CreateChunkRequest(
                parent=doc_name,
                chunk=genai.Chunk(
                    data=genai.ChunkData(string_value=text),
                    custom_metadata=_convert_to_metadata(metadata),
                ),
            )
        )

        if len(batch_request.requests) >= _MAX_REQUEST_PER_CHUNK:
            response = client.batch_create_chunks(batch_request)
            created_chunks.extend(list(response.chunks))
            # Prepare a new batch for next round.
            batch_request = genai.BatchCreateChunksRequest(
                parent=doc_name,
                requests=[],
            )

    # Process left over.
    if len(batch_request.requests) > 0:
        response = client.batch_create_chunks(batch_request)
        created_chunks.extend(list(response.chunks))

    return created_chunks
