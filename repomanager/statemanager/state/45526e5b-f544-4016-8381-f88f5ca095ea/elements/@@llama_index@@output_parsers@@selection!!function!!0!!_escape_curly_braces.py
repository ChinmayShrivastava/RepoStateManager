def _escape_curly_braces(input_string: str) -> str:
    # Replace '{' with '{{' and '}' with '}}' to escape curly braces
    return input_string.replace("{", "{{").replace("}", "}}")
