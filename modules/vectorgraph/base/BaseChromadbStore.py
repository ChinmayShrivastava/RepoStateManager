from modules.vectorgraph.base.types import SimilarityResult, SimilarityResults

class BaseChromadbStore:

    def __init__(
            self
        ):
        pass

    def _top_k(self, query, top_k, collection) -> SimilarityResults:
        _res = collection.query(
            query_texts=[query],
            n_results=top_k
        )
        results = []
        for i in range(top_k):
            result = SimilarityResult(
                similarity=1-_res['distances'][0][i], # changed distance to similarity
                document=_res['documents'][0][i],
                id=int(_res['ids'][0][i]),
                metadata=_res['metadatas'][0][i]
            )
            results.append(result)
        return SimilarityResults(results=results)
    
    def top_k_insights(self, query, k) -> dict:
        return self._top_k(query, k, self.insights_collection).model_dump()
    
    def top_k_chunks(self, query, k) -> dict:
        return self._top_k(query, k, self.chunks_collection).model_dump()
    
    def top_k_ids_insights(self, query, k) -> list:
        return [result.id for result in self._top_k(query, k, self.insights_collection).results]
    
    def top_k_ids_chunks(self, query, k) -> list:
        return [result.id for result in self._top_k(query, k, self.chunks_collection).results]