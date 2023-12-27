def create_llama_chat_agent(
    toolkit: LlamaToolkit,
    llm: BaseLLM,
    callback_manager: Optional[BaseCallbackManager] = None,
    agent_kwargs: Optional[dict] = None,
    **kwargs: Any,
) -> AgentExecutor:
    """Load a chat llama agent given a Llama Toolkit and LLM.

    Args:
        toolkit: LlamaToolkit to use.
        llm: Language model to use as the agent.
        callback_manager: CallbackManager to use. Global callback manager is used if
            not provided. Defaults to None.
        agent_kwargs: Additional key word arguments to pass to the underlying agent
        **kwargs: Additional key word arguments passed to the agent executor

    Returns:
        An agent executor
    """
    # chat agent
    # TODO: explore chat-conversational-react-description
    agent_type = AgentType.CONVERSATIONAL_REACT_DESCRIPTION
    return create_llama_agent(
        toolkit,
        llm,
        agent=agent_type,
        callback_manager=callback_manager,
        agent_kwargs=agent_kwargs,
        **kwargs,
    )
