def fixture_hf_inference_api() -> HuggingFaceInferenceAPI:
    with patch.dict("sys.modules", huggingface_hub=MagicMock()):
        return HuggingFaceInferenceAPI(model_name=STUB_MODEL_NAME)
