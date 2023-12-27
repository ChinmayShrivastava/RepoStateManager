    def override_retrieve(query: str) -> List[NodeWithScore]:
        # replace spaces with underscore in query
        query_url = query.replace(" ", "_")
        return [
            NodeWithScore(
                node=TextNode(
                    text=query,
                    id_="id_100001",
                    metadata={
                        "source": source_url(query),
                    },
                ),
                score=0.9,
            )
        ]
