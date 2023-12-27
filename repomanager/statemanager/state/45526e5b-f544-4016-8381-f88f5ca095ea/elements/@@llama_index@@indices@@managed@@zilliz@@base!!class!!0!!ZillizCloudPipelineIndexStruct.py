class ZillizCloudPipelineIndexStruct(IndexDict):
    """Zilliz Cloud Pipeline's Index Struct."""

    @classmethod
    def get_type(cls) -> IndexStructType:
        """Get index struct type."""
        return IndexStructType.ZILLIZ_CLOUD_PIPELINE
