def parse_pydantic_from_guidance_program(
    program: "Program", cls: Type[Model], verbose: bool = False
) -> Model:
    """Parse output from guidance program.

    This is a temporary solution for parsing a pydantic object out of an executed
    guidance program.

    NOTE: right now we assume the output is the last markdown formatted json block

    NOTE: a better way is to extract via Program.variables, but guidance does not
          support extracting nested objects right now.
          So we call back to manually parsing the final text after program execution
    """
    try:
        output = program.text.split("```json")[-1]
        output = "```json" + output
        if verbose:
            print("Raw output:")
            print(output)
        json_dict = parse_json_markdown(output)
        sub_questions = cls.parse_obj(json_dict)
    except Exception as e:
        raise OutputParserException(
            "Failed to parse pydantic object from guidance program"
        ) from e
    return sub_questions
