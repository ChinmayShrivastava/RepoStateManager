def convert_to_handlebars(text: str) -> str:
    """Convert a python format string to handlebars-style template.

    In python format string, single braces {} are used for variable substitution,
        and double braces {{}} are used for escaping actual braces (e.g. for JSON dict)
    In handlebars template, double braces {{}} are used for variable substitution,
        and single braces are actual braces (e.g. for JSON dict)

    This is currently only used to convert a python format string based prompt template
    to a guidance program template.
    """
    # Replace double braces with a temporary placeholder
    var_left = "TEMP_BRACE_LEFT"
    var_right = "TEMP_BRACE_RIGHT"
    text = text.replace("{{", var_left)
    text = text.replace("}}", var_right)

    # Replace single braces with double braces
    text = text.replace("{", "{{")
    text = text.replace("}", "}}")

    # Replace the temporary placeholder with single braces
    text = text.replace(var_left, "{")
    return text.replace(var_right, "}")
