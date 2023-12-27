    def _completion_with_retry(**kwargs: Any) -> Any:
        if is_gemini:
            history = params["message_history"] if "message_history" in params else []

            generation = client.start_chat(history=history)
            generation_config = dict(kwargs)
            return generation.send_message(
                prompt, stream=stream, generation_config=generation_config
            )
        elif chat:
            generation = client.start_chat(**params)
            if stream:
                return generation.send_message_streaming(prompt, **kwargs)
            else:
                return generation.send_message(prompt, **kwargs)
        else:
            if stream:
                return client.predict_streaming(prompt, **kwargs)
            else:
                return client.predict(prompt, **kwargs)
