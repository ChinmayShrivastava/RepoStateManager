def evaluate(agent: str, model: str, task_name: str, verbose: bool = False) -> bool:
    if task_name in MATH_TASKS:
        task = MATH_TASKS[task_name]()
    elif task_name in BUTTON_TASKS:
        task = BUTTON_TASKS[task_name]()
    else:
        raise ValueError(f"Unknown task {task_name}")

    print("=========================================")
    print(f"Evaluating | {agent} | {model} | {task.message} |")

    llm = get_model(model)
    agent_cls = AGENTS[agent]
    if agent == "react":
        additional_kwargs = {"max_iterations": 10}
    elif agent == "openai":
        additional_kwargs = {"max_function_calls": 10}
    else:
        raise ValueError(f"Unknown agent {agent}")

    agent_ = agent_cls.from_tools(  # type: ignore
        tools=task.tools,
        llm=llm,
        verbose=verbose,
        **additional_kwargs,
    )  # type: ignore
    agent_ = cast(BaseAgent, agent_)
    try:
        actual_response = agent_.chat(task.message).response
        outcome = task.eval_fn(actual_response, task.expected_response)
    except Exception as e:
        if verbose:
            print("Failed due to: ", e)

        actual_response = None
        outcome = False

    if verbose:
        print(f"Expected response: {task.expected_response}")
        print(f"Actual response: {actual_response}")
    print(f"Outcome: {outcome}")
    return outcome
