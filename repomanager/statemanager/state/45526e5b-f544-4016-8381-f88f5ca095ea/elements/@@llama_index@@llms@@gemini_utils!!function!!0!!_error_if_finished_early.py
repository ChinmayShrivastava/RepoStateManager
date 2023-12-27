def _error_if_finished_early(candidate: "glm.Candidate") -> None:  # type: ignore[name-defined] # only until release
    if (finish_reason := candidate.finish_reason) > 1:  # 1=STOP (normally)
        reason = finish_reason.name

        # Safety reasons have more detail, so include that if we can.
        if finish_reason == 3:  # 3=Safety
            relevant_safety = list(
                filter(
                    lambda sr: sr.probability > 1,  # 1=Negligible
                    candidate.safety_ratings,
                )
            )
            reason += f" {relevant_safety}"

        raise RuntimeError(f"Response was terminated early: {reason}")
