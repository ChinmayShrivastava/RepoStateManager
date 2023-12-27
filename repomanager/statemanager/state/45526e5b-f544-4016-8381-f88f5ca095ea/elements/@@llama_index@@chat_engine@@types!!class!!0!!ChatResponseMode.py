class ChatResponseMode(str, Enum):
    """Flag toggling waiting/streaming in `Agent._chat`."""

    WAIT = "wait"
    STREAM = "stream"
