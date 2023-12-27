def create_global_handler(eval_mode: str, **eval_params: Any) -> BaseCallbackHandler:
    """Get global eval handler."""
    if eval_mode == "wandb":
        handler: BaseCallbackHandler = WandbCallbackHandler(**eval_params)
    elif eval_mode == "openinference":
        handler = OpenInferenceCallbackHandler(**eval_params)
    elif eval_mode == "arize_phoenix":
        handler = arize_phoenix_callback_handler(**eval_params)
    elif eval_mode == "honeyhive":
        handler = honeyhive_callback_handler(**eval_params)
    elif eval_mode == "promptlayer":
        handler = PromptLayerHandler(**eval_params)
    elif eval_mode == "simple":
        handler = SimpleLLMHandler(**eval_params)
    else:
        raise ValueError(f"Eval mode {eval_mode} not supported.")

    return handler
