def test_completion_model_basic(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        "llama_index.multi_modal_llms.ReplicateMultiModal.complete", mock_completion
    )

    llm = ReplicateMultiModal(model="llava")
    prompt = "test prompt"
    response = llm.complete(prompt, [ImageDocument()])
    assert "".join(response["output"]) == "Yes, you are allowed "
