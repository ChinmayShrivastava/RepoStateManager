def store_data(education_experience, filename='data.json'):
    data = {}
    for i, element in enumerate(education_experience):
        education_chunks, experience_chunks = final_chunks(element)
        data[i] = {
            "edu_chunks": education_chunks,
            "exp_chunks": experience_chunks
        }
    flname = input('Enter file name: ')
    if flname:
        filename = flname
    with open(f'data/{filename}', 'w') as f:
        json.dump(data, f, indent=4)
