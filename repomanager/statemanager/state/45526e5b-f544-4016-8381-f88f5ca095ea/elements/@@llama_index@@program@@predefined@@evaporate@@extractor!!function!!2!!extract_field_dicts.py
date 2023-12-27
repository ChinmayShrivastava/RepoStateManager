def extract_field_dicts(result: str, text_chunk: str) -> Set:
    """Extract field dictionaries."""
    existing_fields = set()
    result = result.split("---")[0].strip("\n")
    results = result.split("\n")
    results = [r.strip("-").strip() for r in results]
    results = [r[2:].strip() if len(r) > 2 and r[1] == "." else r for r in results]
    for result in results:
        try:
            field = result.split(": ")[0].strip(":")
            value = ": ".join(result.split(": ")[1:])
        except Exception:
            print(f"Skipped: {result}")
            continue
        field_versions = [
            field,
            field.replace(" ", ""),
            field.replace("-", ""),
            field.replace("_", ""),
        ]
        if not any(f.lower() in text_chunk.lower() for f in field_versions):
            continue
        if not value:
            continue
        field = field.lower().strip("-").strip("_").strip(" ").strip(":")
        if field in existing_fields:
            continue
        existing_fields.add(field)

    return existing_fields
