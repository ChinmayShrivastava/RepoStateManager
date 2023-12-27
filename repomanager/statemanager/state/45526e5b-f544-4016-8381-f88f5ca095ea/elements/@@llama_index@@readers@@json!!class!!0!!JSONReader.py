class JSONReader(BaseReader):
    """JSON reader.

    Reads JSON documents with options to help suss out relationships between nodes.

    Args:
        levels_back (int): the number of levels to go back in the JSON tree, 0
          if you want all levels. If levels_back is None, then we just format the
          JSON and make each line an embedding

        collapse_length (int): the maximum number of characters a JSON fragment
          would be collapsed in the output (levels_back needs to be not None)
          ex: if collapse_length = 10, and
          input is {a: [1, 2, 3], b: {"hello": "world", "foo": "bar"}}
          then a would be collapsed into one line, while b would not.
          Recommend starting around 100 and then adjusting from there.

        is_jsonl (Optional[bool]): If True, indicates that the file is in JSONL format.
        Defaults to False.

    """

    def __init__(
        self,
        levels_back: Optional[int] = None,
        collapse_length: Optional[int] = None,
        ensure_ascii: bool = False,
        is_jsonl: Optional[bool] = False,
    ) -> None:
        """Initialize with arguments."""
        super().__init__()
        self.levels_back = levels_back
        self.collapse_length = collapse_length
        self.ensure_ascii = ensure_ascii
        self.is_jsonl = is_jsonl

    def load_data(self, input_file: str) -> List[Document]:
        """Load data from the input file."""
        with open(input_file, encoding="utf-8") as f:
            load_data = []
            if self.is_jsonl:
                for line in f:
                    load_data.append(json.loads(line.strip()))
            else:
                load_data = [json.load(f)]

            documents = []
            for data in load_data:
                # print(data)
                if self.levels_back is None:
                    # If levels_back isn't set, we just format and make each
                    # line an embedding
                    json_output = json.dumps(
                        data, indent=0, ensure_ascii=self.ensure_ascii
                    )
                    lines = json_output.split("\n")
                    useful_lines = [
                        line for line in lines if not re.match(r"^[{}\[\],]*$", line)
                    ]
                    documents.append(Document(text="\n".join(useful_lines)))
                elif self.levels_back is not None:
                    # If levels_back is set, we make the embeddings contain the labels
                    # from further up the JSON tree
                    lines = [
                        *_depth_first_yield(
                            data,
                            self.levels_back,
                            self.collapse_length,
                            [],
                            self.ensure_ascii,
                        )
                    ]
                    documents.append(Document(text="\n".join(lines)))
            return documents
