class StubTokenizer(Tokenizer):
    def encode(self, text: str) -> List[int]:
        return [sum(ord(letter) for letter in word) for word in text.split(" ")]
