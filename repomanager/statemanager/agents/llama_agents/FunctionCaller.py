from llama_index.agent import OpenAIAgent
from tools import tools

class FunctionManager(OpenAIAgent):

    functions_called = []

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