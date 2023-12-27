def generate_strings(num_strings: int = 100, string_length: int = 10) -> List[str]:
    """
    Generate random strings sliced from the paul graham essay of the following form:

    offset 0: [0:string_length], [string_length:2*string_length], ...
    offset 1: [1:1+string_length], [1+string_length:1+2*string_length],...
    ...
    """  # noqa: D415
    content = (
        SimpleDirectoryReader("../../examples/paul_graham_essay/data")
        .load_data()[0]
        .get_content()
    )
    content_length = len(content)

    strings_per_loop = content_length / string_length
    num_loops_upper_bound = int(num_strings / strings_per_loop) + 1
    strings = []

    for offset in range(num_loops_upper_bound + 1):
        ptr = offset % string_length
        while ptr + string_length < content_length:
            strings.append(content[ptr : ptr + string_length])
            ptr += string_length
            if len(strings) == num_strings:
                break

    return strings
