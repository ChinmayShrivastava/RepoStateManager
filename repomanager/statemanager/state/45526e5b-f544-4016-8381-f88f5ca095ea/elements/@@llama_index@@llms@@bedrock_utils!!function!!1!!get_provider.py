def get_provider(model: str) -> Provider:
    provider_name = model.split(".")[0]
    if provider_name not in PROVIDERS:
        raise ValueError(f"Provider {provider_name} for model {model} is not supported")
    return PROVIDERS[provider_name]
