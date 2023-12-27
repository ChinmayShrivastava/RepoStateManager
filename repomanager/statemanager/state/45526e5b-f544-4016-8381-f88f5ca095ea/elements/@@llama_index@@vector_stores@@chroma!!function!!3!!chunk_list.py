def chunk_list(
    lst: List[BaseNode], max_chunk_size: int
) -> Generator[List[BaseNode], None, None]:
    """Yield successive max_chunk_size-sized chunks from lst.

    Args:
        lst (List[BaseNode]): list of nodes with embeddings
        max_chunk_size (int): max chunk size

    Yields:
        Generator[List[BaseNode], None, None]: list of nodes with embeddings
    """
    for i in range(0, len(lst), max_chunk_size):
        yield lst[i : i + max_chunk_size]
