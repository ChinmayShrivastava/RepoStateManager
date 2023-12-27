def test_vllm_call() -> None:
    llm = Vllm(temperature=0)
    output = llm.complete("Say foo:")
    assert isinstance(output.text, str)
