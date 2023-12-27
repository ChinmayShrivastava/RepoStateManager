def _verify_source_safety(__source: Union[str, bytes, CodeType]) -> None:
    pattern = r"_{1,2}\w+_{0,2}"

    if isinstance(__source, CodeType):
        raise RuntimeError("Direct execution of CodeType is forbidden!")
    if isinstance(__source, bytes):
        __source = __source.decode()

    matches = re.findall(pattern, __source)

    if matches:
        raise RuntimeError(
            "Execution of code containing references to private or dunder methods is forbidden!"
        )
