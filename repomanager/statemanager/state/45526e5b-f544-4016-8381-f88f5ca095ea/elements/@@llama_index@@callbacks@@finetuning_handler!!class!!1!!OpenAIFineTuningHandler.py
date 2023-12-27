class OpenAIFineTuningHandler(BaseFinetuningHandler):
    """
    Callback handler for OpenAI fine-tuning.

    This handler will collect all messages
    sent to the LLM, along with their responses. It will then save these messages
    in a `.jsonl` format that can be used for fine-tuning with OpenAI's API.
    """

    def get_finetuning_events(self) -> Dict[str, Dict[str, Any]]:
        events_dict = {}
        for event_id, event in self._finetuning_events.items():
            events_dict[event_id] = {"messages": event[:-1], "response": event[-1]}

        return events_dict

    def save_finetuning_events(self, path: str) -> None:
        """
        Save the finetuning events to a file.

        This saved format can be used for fine-tuning with OpenAI's API.
        The structure for each json line is as follows:
        {
          messages: [
            { rol: "system", content: "Text"},
            { role: "user", content: "Text" },
          ]
        },
        ...
        """
        from llama_index.llms.openai_utils import to_openai_message_dicts

        events_dict = self.get_finetuning_events()
        json_strs = []
        for event_id, event in events_dict.items():
            all_messages = event["messages"] + [event["response"]]
            message_dicts = to_openai_message_dicts(all_messages, drop_none=True)
            event_dict = {"messages": message_dicts}
            if event_id in self._function_calls:
                event_dict["functions"] = self._function_calls[event_id]
            json_strs.append(json.dumps(event_dict))

        with open(path, "w") as f:
            f.write("\n".join(json_strs))
        print(f"Wrote {len(json_strs)} examples to {path}")

    def start_trace(self, trace_id: Optional[str] = None) -> None:
        """Run when an overall trace is launched."""

    def end_trace(
        self,
        trace_id: Optional[str] = None,
        trace_map: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        """Run when an overall trace is exited."""
