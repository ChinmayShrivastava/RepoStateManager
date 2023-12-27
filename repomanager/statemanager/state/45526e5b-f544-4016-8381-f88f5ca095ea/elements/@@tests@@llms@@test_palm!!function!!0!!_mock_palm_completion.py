def _mock_palm_completion(model_name: str, prompt: str, **kwargs: Any) -> str:
    """Mock PaLM completion."""
    completion = MagicMock()
    completion.result = prompt
    completion.candidates = [{"prompt": prompt}]
    return completion
