class Message:
    def __init__(
        self,
        message_id,
        message_text,
        author,
        timestamp,
        parent_message=None,
        child_message=None,
    ):
        self.message_id = message_id
        self.message_text = message_text
        self.author = author
        self.parent_message = parent_message
        self.child_message = child_message
        self.timestamp = timestamp

    def set_child(self, message):
        self.child_message = message

    def set_parent(self, message):
        self.parent_message = message
