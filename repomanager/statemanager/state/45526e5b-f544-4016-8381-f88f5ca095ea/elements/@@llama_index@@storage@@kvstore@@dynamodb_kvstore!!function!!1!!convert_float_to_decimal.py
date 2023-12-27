def convert_float_to_decimal(obj: Any) -> Any:
    if isinstance(obj, List):
        return [convert_float_to_decimal(x) for x in obj]
    elif isinstance(obj, Set):
        return {convert_float_to_decimal(x) for x in obj}
    elif isinstance(obj, Dict):
        return {k: convert_float_to_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, float):
        return Decimal(str(obj))
    else:
        return obj
