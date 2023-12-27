def parse_schema(table: Any) -> Tuple[str, str]:
    key_hash: str | None = None
    key_range: str | None = None

    for key in table.key_schema:
        if key["KeyType"] == "HASH":
            key_hash = key["AttributeName"]
        elif key["KeyType"] == "RANGE":
            key_range = key["AttributeName"]

    if key_hash is not None and key_range is not None:
        return key_hash, key_range
    else:
        raise ValueError("Must be a DynamoDB table with a hash key and sort key.")
