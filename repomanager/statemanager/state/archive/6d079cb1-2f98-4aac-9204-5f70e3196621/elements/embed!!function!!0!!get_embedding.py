def get_embedding(chunks: list, embeddings_model=embeddings_model, batch_size=10):
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        embeddings_ = embeddings_model.embed_documents(batch)
        embeddings.extend(embeddings_)
        print(f"Finished embedding {i} to {i+batch_size} out of {len(chunks)}")
    return chunks, embeddings
