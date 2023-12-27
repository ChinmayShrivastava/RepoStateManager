def test_anthropic_modelname_to_contextsize() -> None:
    with pytest.raises(ValueError):
        anthropic_modelname_to_contextsize("bad name")
