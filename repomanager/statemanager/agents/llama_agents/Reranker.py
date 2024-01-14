from .mods.openaiagent import DEFAULT_MODEL_NAME
from llama_index.llms.openai import OpenAI
from typing import List

CHOICE_SELECT_PROMPT = (
    "A list of documents is shown below. Each document has a number next to it along "
    "with a summary of the document. A question is also provided. \n"
    "Respond with the numbers of the documents "
    "you should consult to answer the question, in order of relevance, as well \n"
    "as the relevance score. The relevance score is a number from 1-10 based on "
    "how relevant you think the document is to the question.\n"
    "Do not include any documents that are not relevant to the question. \n"
    "Leave out redundant documents. \n"
    "Example format: \n"
    "Document 1:\n<summary of document 1>\n\n"
    "Document 2:\n<summary of document 2>\n\n"
    "...\n\n"
    "Document 10:\n<summary of document 10>\n\n"
    "Question: <question>\n"
    "Answer:\n"
    "Doc: 9, Relevance: 7\n"
    "Doc: 3, Relevance: 4\n"
    "Doc: 7, Relevance: 3\n\n"
    "Let's try this now: \n\n"
    "{context_str}\n"
    "Question: {query_str}\n"
    "Answer:\n"
)

class LLMReranker():
    def __init__(self, llm = None) -> None:
        self.llm = llm if llm is not None else OpenAI(DEFAULT_MODEL_NAME)

    def _prepare_docs(self, docs: List[str]) -> str:
        return "\n".join([f"Document {i}:\n{document}\n" for i, document in enumerate(docs, 1)])

    def rerank(self, query: str, documents: List[str]) -> List[str]:
        """Reranks a list of documents based on a question"""
        if len(documents) == 0:
            return None
        doc_str = self._prepare_docs(documents)
        _prompt = CHOICE_SELECT_PROMPT.format(context_str=doc_str, query_str=query)
        r = self.llm.complete(_prompt)
        r = r.text.split("\n")
        # return list of tuples, (doc_id, relevance_score)
        r = [i for i in r if i.startswith("Doc: ")]
        r = [i.split(", Relevance: ") for i in r]
        r = [(int(i[0].split(": ")[1]), int(i[1])) for i in r]
        r = sorted(r, key=lambda x: x[1], reverse=True)
        r = [i[0] for i in r]
        print(len(documents), len(r))
        print(r)
        if len(r) == 0:
            return None
        return [documents[i-1] for i in r]