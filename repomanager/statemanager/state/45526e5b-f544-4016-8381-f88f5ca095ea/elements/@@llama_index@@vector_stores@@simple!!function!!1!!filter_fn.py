    def filter_fn(node_id: str) -> bool:
        metadata = metadata_lookup_fn(node_id)
        for filter_ in filter_list:
            metadata_value = metadata.get(filter_.key, None)
            if metadata_value is None:
                return False
            elif isinstance(metadata_value, list):
                if filter_.value not in metadata_value:
                    return False
            elif isinstance(metadata_value, (int, float, str, bool)):
                if metadata_value != filter_.value:
                    return False
        return True
