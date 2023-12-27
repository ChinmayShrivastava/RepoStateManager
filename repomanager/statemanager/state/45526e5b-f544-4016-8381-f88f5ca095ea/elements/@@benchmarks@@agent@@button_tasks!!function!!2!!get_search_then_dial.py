def get_search_then_dial() -> Task:
    phone = Phone()

    dial_digit_tool = FunctionTool.from_defaults(fn=phone.dial_digit)
    enter_tool = FunctionTool.from_defaults(fn=phone.enter)

    return Task(
        message="Dial the number for john smith, then hit enter.",
        expected_response="2135",
        tools=[dial_digit_tool, enter_tool, search_number_tool],
        eval_fn=phone.evaluate,
    )
