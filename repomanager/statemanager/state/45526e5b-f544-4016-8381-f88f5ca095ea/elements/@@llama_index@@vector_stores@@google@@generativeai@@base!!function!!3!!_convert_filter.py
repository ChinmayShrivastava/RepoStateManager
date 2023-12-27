def _convert_filter(fs: Optional[MetadataFilters]) -> Dict[str, Any]:
    if fs is None:
        return {}
    assert isinstance(fs, MetadataFilters)
    return {f.key: f.value for f in fs.filters}
