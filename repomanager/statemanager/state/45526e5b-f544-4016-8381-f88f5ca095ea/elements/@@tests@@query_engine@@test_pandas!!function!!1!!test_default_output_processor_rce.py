def test_default_output_processor_rce(tmp_path: Path) -> None:
    """
    Test that output processor prevents RCE.
    https://github.com/run-llama/llama_index/issues/7054 .
    """
    df = pd.DataFrame(
        {
            "city": ["Toronto", "Tokyo", "Berlin"],
            "population": [2930000, 13960000, 3645000],
        }
    )

    tmp_file = tmp_path / "pwnnnnn"

    injected_code = f"__import__('os').system('touch {tmp_file}')"
    default_output_processor(injected_code, df)

    assert not tmp_file.is_file(), "file has been created via RCE!"
