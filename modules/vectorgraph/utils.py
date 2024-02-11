def format_trace(query, chunks, response, to_print=True):
    trace = ''
    if to_print:
        # add query in yellow
        trace += f"\033[93mQuery: {query}\033[0m\n"
        trace += "\n"
        # add chunks in green
        trace += "\033[92mChunks:\n"
        for chunk in chunks:
            trace += f"{chunk}\033[0m\n"
        trace += "\n"
        # add response in blue
        trace += "\033[94mResponse:\n"
        trace += response
        trace += "\033[0m"
    else:
        trace += f"Query: {query}\n"
        trace += "\n"
        trace += "Chunks:\n"
        for chunk in chunks:
            trace += f"{chunk}\n"
        trace += "\n"
        trace += "Response:\n"
        trace += response
    return trace