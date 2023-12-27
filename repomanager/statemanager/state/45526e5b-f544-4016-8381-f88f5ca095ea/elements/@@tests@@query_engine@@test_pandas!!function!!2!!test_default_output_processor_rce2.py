def test_default_output_processor_rce2() -> None:
    """
    Test that output processor prevents RCE.
    https://github.com/run-llama/llama_index/issues/7054#issuecomment-1829141330 .
    """
    df = pd.DataFrame(
        {
            "city": ["Toronto", "Tokyo", "Berlin"],
            "population": [2930000, 13960000, 3645000],
        }
    )

    injected_code = "().__class__.__mro__[-1].__subclasses__()[137].__init__.__globals__['system']('ls')"

    output = default_output_processor(injected_code, df)

    assert (
        "Execution of code containing references to private or dunder methods is forbidden!"
        in output
    ), "Injected code executed successfully!"
