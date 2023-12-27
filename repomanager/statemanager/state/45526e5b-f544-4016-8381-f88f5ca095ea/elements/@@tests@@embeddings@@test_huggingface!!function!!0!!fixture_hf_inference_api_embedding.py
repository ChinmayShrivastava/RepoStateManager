def fixture_hf_inference_api_embedding() -> HuggingFaceInferenceAPIEmbedding:
    with patch.dict("sys.modules", huggingface_hub=MagicMock()):
        return HuggingFaceInferenceAPIEmbedding(model_name=STUB_MODEL_NAME)
