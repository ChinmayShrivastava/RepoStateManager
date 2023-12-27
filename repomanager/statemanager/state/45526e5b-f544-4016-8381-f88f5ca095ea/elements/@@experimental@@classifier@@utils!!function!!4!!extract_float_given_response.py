def extract_float_given_response(response: str, n: int = 1) -> Optional[float]:
    """Extract number given the GPT-generated response.

    Used by tree-structured indices.

    """
    numbers = re.findall(r"\d+\.\d+", response)
    if len(numbers) == 0:
        # if no floats, try extracting ints, and convert to float
        new_numbers = extract_numbers_given_response(response, n=n)
        if new_numbers is None:
            return None
        else:
            return float(numbers[0])
    else:
        return float(numbers[0])
