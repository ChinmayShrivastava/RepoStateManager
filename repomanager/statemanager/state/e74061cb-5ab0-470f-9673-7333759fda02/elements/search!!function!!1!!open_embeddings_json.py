def open_embeddings_json():
    with open('data/embeddings.json', 'r') as f:
        embeddings = json.load(f)
    return embeddings
