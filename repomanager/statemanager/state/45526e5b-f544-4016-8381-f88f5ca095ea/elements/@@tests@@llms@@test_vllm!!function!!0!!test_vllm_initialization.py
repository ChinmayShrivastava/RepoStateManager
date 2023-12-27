def test_vllm_initialization() -> None:
    llm = Vllm()
    assert llm.class_name() == "Vllm"
