def benchmark(
    agents: List[str] = list(AGENTS.keys()),
    models: List[str] = ALL_MODELS,
    tasks: List[str] = ALL_TASKS,
    verbose: bool = False,
    output: str = "results.csv",
    save: bool = True,
) -> pd.DataFrame:
    data = []
    for agent in agents:
        for model in models:
            for task in tasks:
                if not is_valid_combination(agent, model):
                    continue
                outcome = evaluate(agent, model, task, verbose)
                data.append(
                    {
                        "agent": agent,
                        "model": model,
                        "task": task,
                        "outcome": outcome,
                    }
                )
    df = pd.DataFrame(data)
    if save:
        df.to_csv(output)
    return df
