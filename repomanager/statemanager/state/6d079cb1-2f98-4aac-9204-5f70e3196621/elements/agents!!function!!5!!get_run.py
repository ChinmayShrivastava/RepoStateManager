def get_run(runid, threadid):
    run = client.beta.threads.runs.retrieve(
        thread_id=threadid,
        run_id=runid
    )
    return run
