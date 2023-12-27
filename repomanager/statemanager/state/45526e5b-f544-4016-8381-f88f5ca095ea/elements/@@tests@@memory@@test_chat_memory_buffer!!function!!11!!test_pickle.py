def test_pickle() -> None:
    """Unpickleable tiktoken tokenizer should be circumvented when pickling."""
    memory = ChatMemoryBuffer.from_defaults()
    bytes_ = pickle.dumps(memory)
    assert isinstance(pickle.loads(bytes_), ChatMemoryBuffer)
