def test_to_llama_similarities_from_df_w_distance() -> None:
    data = dict(data_stub)
    distances: List[float] = [np.log(4 / 3), np.log(2), np.log(4)]

    # lance provides '_distance' by natural sort test should as well
    natural_sort = distances.copy()
    natural_sort.sort()
    assert np.array_equal(natural_sort, distances)  # gut check setup

    data["_distance"] = distances
    df = pd.DataFrame(data)
    llama_sim_array = _to_llama_similarities(df)
    assert np.allclose(llama_sim_array, [0.75, 0.5, 0.25])
