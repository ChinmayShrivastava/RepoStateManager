def add_files(file_names_raw):
    files = []
    for file_name_raw in file_names_raw:
        file = client.files.create(
            file=open(file_name_raw["file_name"], 'rb'),
            purpose='assistants'
            )
        files.append(file.id)
    return files
