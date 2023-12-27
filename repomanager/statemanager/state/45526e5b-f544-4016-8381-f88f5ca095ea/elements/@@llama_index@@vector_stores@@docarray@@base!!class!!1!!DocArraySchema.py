        class DocArraySchema(BaseDoc):
            id: Optional[ID] = None
            text: Optional[str] = None
            metadata: Optional[dict] = None
            embedding: NdArray = Field(**embeddings_params)
