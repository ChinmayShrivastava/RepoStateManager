def test_to_llama_similarities_from_df_w_score() -> None:
    data = dict(data_stub)
    scores: List[float] = [9, 9 - np.log(2), 9 - np.log(4)]

    # lance provides 'score' in reverse natural sort test should as well
    reversed_sort = scores.copy()
    reversed_sort.sort(reverse=True)
    assert np.array_equal(reversed_sort, scores)  # gut check setup

    data["score"] = scores
    df = pd.DataFrame(data)
    llama_sim_array = _to_llama_similarities(df)
    assert np.allclose(llama_sim_array, [1, 0.5, 0.25])
