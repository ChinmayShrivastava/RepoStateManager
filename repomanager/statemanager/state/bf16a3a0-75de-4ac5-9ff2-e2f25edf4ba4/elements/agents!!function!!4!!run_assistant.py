def run_assistant(assistantid, threadid):
    run = client.beta.threads.runs.create(
        thread_id=threadid,
        assistant_id=assistantid
    )
    return run
