def convert_decimal_to_int_or_float(obj: Any) -> Any:
    if isinstance(obj, List):
        return [convert_decimal_to_int_or_float(x) for x in obj]
    elif isinstance(obj, Set):
        return {convert_decimal_to_int_or_float(x) for x in obj}
    elif isinstance(obj, Dict):
        return {k: convert_decimal_to_int_or_float(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return num if (num := int(obj)) == obj else float(obj)
    else:
        return obj
