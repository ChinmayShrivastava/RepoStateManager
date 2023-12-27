class LLMLookaheadAnswerInserter(BaseLookaheadAnswerInserter):
    """LLM Lookahead answer inserter.

    Takes in a lookahead response and a list of query tasks, and the
        lookahead answers, and inserts the answers into the lookahead response.

    Args:
        service_context (ServiceContext): Service context.

    """

    def __init__(
        self,
        service_context: Optional[ServiceContext] = None,
        answer_insert_prompt: Optional[BasePromptTemplate] = None,
    ) -> None:
        """Init params."""
        self._service_context = service_context or ServiceContext.from_defaults()
        self._answer_insert_prompt = (
            answer_insert_prompt or DEFAULT_ANSWER_INSERT_PROMPT
        )

    def _get_prompts(self) -> Dict[str, Any]:
        """Get prompts."""
        return {
            "answer_insert_prompt": self._answer_insert_prompt,
        }

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        if "answer_insert_prompt" in prompts:
            self._answer_insert_prompt = prompts["answer_insert_prompt"]

    def insert(
        self,
        response: str,
        query_tasks: List[QueryTask],
        answers: List[str],
        prev_response: Optional[str] = None,
    ) -> str:
        """Insert answers into response."""
        prev_response = prev_response or ""

        query_answer_pairs = ""
        for query_task, answer in zip(query_tasks, answers):
            query_answer_pairs += f"Query: {query_task.query_str}\nAnswer: {answer}\n"

        return self._service_context.llm.predict(
            self._answer_insert_prompt,
            lookahead_response=response,
            query_answer_pairs=query_answer_pairs,
            prev_response=prev_response,
        )
