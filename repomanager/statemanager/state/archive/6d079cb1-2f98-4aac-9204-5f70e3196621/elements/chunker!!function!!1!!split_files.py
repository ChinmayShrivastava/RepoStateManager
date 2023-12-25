def split_files(files):
    split_files = []
    for file in files:
        split_files.extend(file.split('!@#'))
    return split_files
