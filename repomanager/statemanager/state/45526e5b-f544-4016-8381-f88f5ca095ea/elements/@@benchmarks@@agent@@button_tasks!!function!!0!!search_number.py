def search_number(first_name: str, last_name: str) -> str:
    """Search for a person by first and last name."""
    if first_name == "John" and last_name == "Smith":
        return "2135"
    else:
        return "No results found. Please capitalize both first and last name."
