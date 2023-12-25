def save_embeddings(data):
    embeddings_json = {}
    for i, element in enumerate(data):
        print(f"Saving embeddings for element {i}")
        edu_embeddings = get_embedding(data[element]["edu_chunks"])[1]
        exp_embeddings = get_embedding(data[element]["exp_chunks"])[1]
        for j, edu_embedding in enumerate(edu_embeddings):
            embeddings_json[f"{i}_edu_{j}"] = edu_embedding
        for j, exp_embedding in enumerate(exp_embeddings):
            embeddings_json[f"{i}_exp_{j}"] = exp_embedding
    with open('data/embeddings.json', 'w') as f:
        json.dump(embeddings_json, f, indent=4)
