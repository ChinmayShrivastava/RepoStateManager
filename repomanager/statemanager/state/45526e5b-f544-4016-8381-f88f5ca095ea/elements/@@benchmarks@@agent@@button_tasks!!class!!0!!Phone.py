class Phone:
    def __init__(self) -> None:
        self.number = ""
        self.entered = False

    def dial_digit(self, number: str) -> None:
        """Dial a digit  on the phone."""
        assert len(number) == 1 and number.isdigit()
        self.number += number

    def enter(self) -> None:
        """Press the enter key on the phone."""
        if self.entered:
            raise Exception("Already entered")

        self.entered = True

    def evaluate(self, response: str, expected_response: str) -> bool:
        return self.number == expected_response and self.entered
