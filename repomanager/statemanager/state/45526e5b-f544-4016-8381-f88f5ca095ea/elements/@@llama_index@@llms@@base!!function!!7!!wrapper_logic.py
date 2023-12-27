        def wrapper_logic(_self: Any) -> Generator[CallbackManager, None, None]:
            callback_manager = getattr(_self, "callback_manager", None)
            if not isinstance(callback_manager, CallbackManager):
                raise ValueError(
                    "Cannot use llm_completion_callback on an instance "
                    "without a callback_manager attribute."
                )

            yield callback_manager
