def create_assistant(name, description, file_ids, model='gpt-3.5-turbo-1106'):
    assistant = client.beta.assistants.create(
        name=name,
        description=description,
        model=model,
        tools=[{"type": "retrieval"}],
        file_ids=file_ids
    )
    return assistant
