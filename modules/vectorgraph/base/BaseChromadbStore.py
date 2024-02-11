from modules.vectorgraph.base.types import SimilarityResult, SimilarityResults

class BaseChromadbStore:

    def __init__(
            self
        ):
        pass

    def _top_k(self, query, k) -> SimilarityResults:
        _res = self.collection.query(
            query_texts=[query],
            n_results=k
        )
        results = []
        for i in range(k):
            result = SimilarityResult(
                similarity=1-_res['distances'][0][i], # change distance to similarity
                document=_res['documents'][0][i],
                id=int(_res['ids'][0][i]),
                metadata=_res['metadatas'][0][i]
            )
            results.append(result)
        return SimilarityResults(results=results)
    
    def top_k(self, query, k) -> dict:
        return self._top_k(query, k).model_dump()
    
    def top_k_ids(self, query, k) -> list:
        return [result.id for result in self._top_k(query, k).results]