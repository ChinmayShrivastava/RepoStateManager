def get_dial_then_enter() -> Task:
    phone = Phone()

    dial_digit_tool = FunctionTool.from_defaults(fn=phone.dial_digit)
    enter_tool = FunctionTool.from_defaults(fn=phone.enter)

    return Task(
        message="Dial the number 4151 then hit enter.",
        expected_response="4151",
        tools=[dial_digit_tool, enter_tool],
        eval_fn=phone.evaluate,
    )
