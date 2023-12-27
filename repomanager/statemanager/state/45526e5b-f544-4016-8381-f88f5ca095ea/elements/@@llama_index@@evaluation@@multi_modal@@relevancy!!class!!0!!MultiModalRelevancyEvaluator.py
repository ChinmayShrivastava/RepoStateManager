class MultiModalRelevancyEvaluator(BaseEvaluator):
    """Relevancy evaluator.

    Evaluates the relevancy of retrieved image and textual contexts and response to a query.
    This evaluator considers the query string, retrieved contexts, and response string.

    Args:
        multi_modal_llm(Optional[MultiModalLLM]):
            The Multi-Modal LLM Judge to use for evaluations.
        raise_error(Optional[bool]):
            Whether to raise an error if the response is invalid.
            Defaults to False.
        eval_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for evaluation.
        refine_template(Optional[Union[str, BasePromptTemplate]]):
            The template to use for refinement.
    """

    def __init__(
        self,
        multi_modal_llm: Union[MultiModalLLM, None] = None,
        raise_error: bool = False,
        eval_template: Union[str, BasePromptTemplate, None] = None,
        refine_template: Union[str, BasePromptTemplate, None] = None,
    ) -> None:
        """Init params."""
        self._multi_modal_llm = multi_modal_llm or OpenAIMultiModal(
            model="gpt-4-vision-preview", max_new_tokens=1000
        )
        self._raise_error = raise_error

        self._eval_template: BasePromptTemplate
        if isinstance(eval_template, str):
            self._eval_template = PromptTemplate(eval_template)
        else:
            self._eval_template = eval_template or DEFAULT_EVAL_TEMPLATE

        self._refine_template: BasePromptTemplate
        if isinstance(refine_template, str):
            self._refine_template = PromptTemplate(refine_template)
        else:
            self._refine_template = refine_template or DEFAULT_REFINE_TEMPLATE

    def _get_prompts(self) -> PromptDictType:
        """Get prompts."""
        return {
            "eval_template": self._eval_template,
            "refine_template": self._refine_template,
        }

    def _update_prompts(self, prompts: PromptDictType) -> None:
        """Update prompts."""
        if "eval_template" in prompts:
            self._eval_template = prompts["eval_template"]
        if "refine_template" in prompts:
            self._refine_template = prompts["refine_template"]

    def evaluate(
        self,
        query: Union[str, None] = None,
        response: Union[str, None] = None,
        contexts: Union[Sequence[str], None] = None,
        image_paths: Union[List[str], None] = None,
        image_urls: Union[List[str], None] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        """Evaluate whether the multi-modal contexts and response are relevant to the query."""
        del kwargs  # Unused

        if query is None or contexts is None or response is None:
            raise ValueError("query, contexts, and response must be provided")

        context_str = "\n\n".join(contexts)
        evaluation_query_str = f"Question: {query}\nResponse: {response}"
        fmt_prompt = self._eval_template.format(
            context_str=context_str, query_str=evaluation_query_str
        )

        if image_paths:
            image_nodes = [
                ImageNode(image_path=image_path) for image_path in image_paths
            ]
        if image_urls:
            image_nodes = [ImageNode(image_url=image_url) for image_url in image_urls]

        response_obj = self._multi_modal_llm.complete(
            prompt=fmt_prompt,
            image_documents=image_nodes,
        )

        raw_response_txt = str(response_obj)

        if "yes" in raw_response_txt.lower():
            passing = True
        else:
            if self._raise_error:
                raise ValueError("The response is invalid")
            passing = False

        return EvaluationResult(
            query=query,
            response=response,
            passing=passing,
            score=1.0 if passing else 0.0,
            feedback=raw_response_txt,
        )

    async def aevaluate(
        self,
        query: Union[str, None] = None,
        response: Union[str, None] = None,
        contexts: Union[Sequence[str], None] = None,
        image_paths: Union[List[str], None] = None,
        image_urls: Union[List[str], None] = None,
        **kwargs: Any,
    ) -> EvaluationResult:
        """Async evaluate whether the multi-modal contexts and response are relevant to the query."""
        del kwargs  # Unused

        if query is None or contexts is None or response is None:
            raise ValueError("query, contexts, and response must be provided")

        context_str = "\n\n".join(contexts)
        evaluation_query_str = f"Question: {query}\nResponse: {response}"
        fmt_prompt = self._eval_template.format(
            context_str=context_str, query_str=evaluation_query_str
        )

        if image_paths:
            image_nodes = [
                ImageNode(image_path=image_path) for image_path in image_paths
            ]
        if image_urls:
            image_nodes = [ImageNode(image_url=image_url) for image_url in image_urls]

        response_obj = await self._multi_modal_llm.acomplete(
            prompt=fmt_prompt,
            image_documents=image_nodes,
        )

        raw_response_txt = str(response_obj)

        if "yes" in raw_response_txt.lower():
            passing = True
        else:
            if self._raise_error:
                raise ValueError("The response is invalid")
            passing = False

        return EvaluationResult(
            query=query,
            response=response,
            passing=passing,
            score=1.0 if passing else 0.0,
            feedback=raw_response_txt,
        )
