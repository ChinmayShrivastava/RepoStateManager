def chunking_pipeline(folder='data', filename='data.json'):
    files = open_files(folder)
    split_files = split_files(files)
    education_experience = extract_education_and_experience(split_files)
    store_data(education_experience, filename)
