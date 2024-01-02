from llama_index.agent import OpenAIAgent
from tools import tools
from llama_index.llms.openai import OpenAI
from llama_index.llms.llm import LLM
from llama_index.memory.chat_memory_buffer import ChatMemoryBuffer
from llama_index.memory.types import BaseMemory
from llama_index.objects.base import ObjectRetriever
from llama_index.tools import BaseTool
from llama_index.callbacks import CallbackManager
from llama_index.llms.base import ChatMessage
from typing import Any, List, Optional, Type

AGENT_DESCRIPTION = (
    "As a function caller, you have access to functions that can help access a code library named 'repo manager'."
    "For the user query, call the functions for the relevant information, and answer the query."
    "Collect sufficient information before answering the query."
    "If one tool doesn't give you the information you need, try another tool."
    "Always make sure that you have the right information before answering the query."
    "If the user query is insufficient, answer as best as you can by searching for other relevant information related to the query."
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