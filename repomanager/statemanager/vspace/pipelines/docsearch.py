from agents.llama_agents.Reranker import LLMReranker
from defaults.vsearch import DISTANCE_THRESHOLD_pinecone

def get_docs(
    query: str,
    vs,
    G,
    top_k: int = 25,
    to_return: int = 2,
    ):
    res = vs.search_all(query, top_k=top_k)
    matches = res['matches']
    # nodes = [x["node"] for x in res['metadatas'][0]]
    nodes = [x["metadata"]['node'] for x in matches]
    distances = [x["score"] for x in matches]
    docs = []
    for node in nodes:
        docs.append(G.get_node_metadata(node)["content"])
    i = 0
    _new_docs = []
    for doc, dist in zip(docs, distances):
        if dist < DISTANCE_THRESHOLD_pinecone:
            continue
        if i>=5:
            break
        if len(doc.split()) < 10:
            continue
        if len(doc.split()) > 200:
            doc = " ".join(doc.split()[:200])
        _new_docs.append(doc)
        i = i + 1
    reranker = LLMReranker()
    reranked_docs = reranker.rerank(query, _new_docs)
    docs = reranked_docs[:to_return]
    return docs