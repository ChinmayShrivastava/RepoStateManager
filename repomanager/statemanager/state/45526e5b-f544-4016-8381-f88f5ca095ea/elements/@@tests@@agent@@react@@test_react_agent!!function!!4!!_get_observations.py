def _get_observations(task: Task) -> List[str]:
    obs_steps = [
        s
        for s in task.extra_state["current_reasoning"]
        if isinstance(s, ObservationReasoningStep)
    ]
    return [s.observation for s in obs_steps]
