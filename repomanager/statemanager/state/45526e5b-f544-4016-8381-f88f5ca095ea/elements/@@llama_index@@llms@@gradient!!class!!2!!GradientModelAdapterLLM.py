class GradientModelAdapterLLM(_BaseGradientLLM):
    model_adapter_id: str = Field(
        description="The id of the model adapter to use.",
    )

    def __init__(
        self,
        *,
        access_token: Optional[str] = None,
        host: Optional[str] = None,
        max_tokens: Optional[int] = None,
        model_adapter_id: str,
        workspace_id: Optional[str] = None,
        callback_manager: Optional[CallbackManager] = None,
        is_chat_model: bool = False,
    ) -> None:
        super().__init__(
            access_token=access_token,
            host=host,
            max_tokens=max_tokens,
            model_adapter_id=model_adapter_id,
            workspace_id=workspace_id,
            callback_manager=callback_manager,
            is_chat_model=is_chat_model,
        )
        self._model = self._gradient.get_model_adapter(
            model_adapter_id=model_adapter_id
        )
