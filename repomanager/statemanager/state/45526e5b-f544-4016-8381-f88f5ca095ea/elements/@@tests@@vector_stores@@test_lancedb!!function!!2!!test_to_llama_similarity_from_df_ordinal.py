def test_to_llama_similarity_from_df_ordinal() -> None:
    data = dict(data_stub)
    df = pd.DataFrame(data)
    llama_sim_array = _to_llama_similarities(df)
    assert np.allclose(llama_sim_array, [1, 0.5, 0])
