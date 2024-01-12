from .mods.openaiagent import OpenAIAgent, DEFAULT_MODEL_NAME
from .tools import tools
from llama_index.llms.openai import OpenAI
from llama_index.llms.llm import LLM
from llama_index.memory.chat_memory_buffer import ChatMemoryBuffer
from llama_index.memory.types import BaseMemory
from llama_index.objects.base import ObjectRetriever
from llama_index.tools import BaseTool
from llama_index.callbacks import CallbackManager
from llama_index.llms.base import ChatMessage
from typing import Any, List, Optional, Type
from llama_index.tools import FunctionTool
from pydantic import BaseModel
from llama_index.agent import OpenAIAssistantAgent
from llms.parse import parse_trilet

# AGENT_DESCRIPTION = (
#     "As a function caller, you have access to functions that can help access a code library named 'Llama Index'."
#     "For the user query, call the functions for the relevant information, and answer the query."
#     "Collect sufficient information before answering the query."
#     "If one tool doesn't give you the information you need, try another tool."
#     "Always make sure that you have the right information before answering the query."
#     "If the user query is insufficient, answer as best as you can by searching for other relevant information related to the query."
# )

LLAMA_INDEX_KOWLEDGE_CONTEXT = "Provides relevant code and examples of python library llama index"

QUERY_TRANSFORMER = """The original query is as follows: {query}
We have an opportunity to answer some, or all of the query from a knowledge source.
Context information for the knowledge source is provided below.
Given the context, return a list of new queries that can be answered from the context.
As an example:
===
Query: How many Grand Slam titles does the winner of the 2020 Australian Open have?
Knowledge source context: Provides information about the winners of the 2020 Australian Open
New queries: (2020 australian open winner, australian open grand slam total titles 2020)
===
Query: What is the current population of the city in which Paul Graham found his first company, Viaweb?
Knowledge source context: Provides information about Paul Graham's
professional career, including the startups he's founded.
New queries: (viaweb headquarters, paul graham viaweb headquarter location)
===
Query: {query}
Knowledge source context: {knowledge_context}
New queries: """

AGENT_DESCRIPTION = (
    "As a function caller, you have access to functions that can help access a code library named 'Llama Index'.\n"
    "For the given query, call the functions for the relevant information.\n"
    "Collect sufficient information before answering the query.\n"
    "If one tool doesn't give you the information you need, try another tool.\n"
    "Don't call the same information twice.\n"
    '----------'
    "Do not answer the query. Your job is to collect the information.\n"
    'Return \'[DONE]\' when you have collected sufficient information.\n'
)

AGENT_INSTRUCTIONS = (
    "You are an on call engineer on the public code library 'Llama Index'."
    "Help the user by answering their queries."
    "Based on the context info from the tools, answer the query."
    "Be succinct and direct, and abstract away what you don't know. Don't generate unknown information."
    "Be helpful to the user by providing example where you can."
    "Don't generate long answers, no-one likes long answers."
)

BREAK_QUERY = """You can request the code and functionality when needed but you need to provide a rich and succinct query in exchange.

Rephrase the user query into one question to get back context information to answer the query. Break the functions/classes/methods for better questioning.
----------
Be very specific and direct in what you ask.
Don't use any redundant words.
----------
User query: {query}
Rephrased query:"""

CHOICE_SELECT_PROMPT = (
    "A list of documents is shown below. Each document has a number next to it along "
    "with a summary of the document. A question is also provided. \n"
    "Respond with the numbers of the documents "
    "you should consult to answer the question, in order of relevance, as well \n"
    "as the relevance score. The relevance score is a number from 1-10 based on "
    "how relevant you think the document is to the question.\n"
    "Do not include any documents that are not relevant to the question. \n"
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
    def __init__(self, llm: LLM) -> None:
        self.llm = llm

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

# async def get_context(query, verbose=True) -> str:
#     """Returns the context for the query"""
#     fm = FunctionManager.from_tools(
#         tools=tools,
#         verbose=verbose,
#         max_function_calls=5,
#         llm=OpenAI('gpt-4'),
#     )
#     r = await fm.achat(query,
#     chat_history=fm.chat_history)
#     response = ""
#     for message in fm.memory.chat_history:
#         if message.role.value == "tool":
#             response += message.content+'\n'+"----------"+'\n'
#     response = 'Information from the codebase:\n'+response
#     return response

def get_context(query, verbose=True) -> List[str]:
    """Returns the context for the query"""
    fm = FunctionManager.from_tools(
        tools=tools,
        verbose=verbose,
        max_function_calls=2,
        llm=OpenAI('gpt-3.5-turbo'),
    )
    r = fm.chat(query,
    chat_history=fm.chat_history)
    chat_history = fm.memory.chat_store.store['chat_history']
    # print in red
    docs = []
    for message in chat_history:
        if message.role == "tool":
            docs.append(message.content)
    # top 1 reraanked
    llm = LLMReranker(OpenAI(DEFAULT_MODEL_NAME))
    _context = llm.rerank(query, docs)
    if _context is None:
        return ''
    # response = "The following is relevant information to help answer the query:\n"
    # response += "----------\n"
    # response += "Query: "+query+"\n"
    # response += "Context: "+_context+"\n"
    # response += "----------\n"
    return _context

class GetContext(BaseModel):
    # doesn't take any input
    pass

context_tool = FunctionTool.from_defaults(
    fn=get_context,
    name="get_context",
    description="Returns the context for the query",
    fn_schema=GetContext,
    tool_metadata=None,
    async_fn=None,
)

class FunctionManager(OpenAIAgent):

    functions_called = []
    chat_history = [ChatMessage(role="system", content=AGENT_DESCRIPTION)]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.tools = tools

    def get_function_name(self, step_result):
        """Returns the function name that was called after running a step"""
        if step_result is not None:
            return (
                step_result.output.sources[-1].content,
                step_result.output.sources[-1].tool_name, 
                step_result.output.sources[-1].raw_input,
                step_result.output.sources[-1].raw_output,
                )
        else:
            return None
        
    def run_step_and_get_function_name(self):
        """Runs a step and returns the function name that was called"""
        tid = self.get_tid_from_chat()
        step_result = self.run_step(tid)
        # add function name to list of functions called
        self.functions_called.append(self.get_function_name(step_result))
        return self.functions_called
    
    def get_tid_from_chat(self):
        """Returns the tid from a chat"""
        return list(self.state.task_dict.keys())[0]
    
class GodFather(OpenAIAgent):
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.llm = OpenAI(DEFAULT_MODEL_NAME)
        self.llm4 = OpenAI('gpt-4')

    def break_query(self, query):
        """Breaks a query into smaller queries"""
        _prompt = QUERY_TRANSFORMER.format(query=query, knowledge_context=LLAMA_INDEX_KOWLEDGE_CONTEXT)
        r = self.llm.complete(_prompt).text
        queries = parse_trilet(r)
        return queries