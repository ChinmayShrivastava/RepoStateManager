def extract_education_and_experience(split_files):
    education_experience = []
    for file in split_files:
        split_file = file.split('##')
        education_experience.append(split_file)
    return education_experience
