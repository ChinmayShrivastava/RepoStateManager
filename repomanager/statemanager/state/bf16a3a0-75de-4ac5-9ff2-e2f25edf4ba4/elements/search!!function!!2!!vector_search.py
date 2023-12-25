def vector_search(query, embeddings=embeddings, datajson=datajson):
    vector = get_embedding([query])[1][0]
    results = []
    for key in embeddings:
        result = {}
        result["key"] = key
        result["score"] = cosine_similarity(vector, embeddings[key])
        results.append(result)
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    # for each key in results, get the corresponding data
    for result in results:
        key = result["key"]
        key_split = key.split("_")
        index = int(key_split[0])
        edu_or_exp = key_split[1]
        edu_or_exp_index = int(key_split[2])
        result["data"] = datajson[f'{index}'][f"{edu_or_exp}_chunks"][edu_or_exp_index]
    print(results[0]["data"])
    return results
