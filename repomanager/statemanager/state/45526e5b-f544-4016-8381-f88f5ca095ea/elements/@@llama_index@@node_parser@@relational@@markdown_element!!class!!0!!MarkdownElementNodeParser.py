class MarkdownElementNodeParser(BaseElementNodeParser):
    """Markdown element node parser.

    Splits a markdown document into Text Nodes and Index Nodes corresponding to embedded objects
    (e.g. tables).

    """

    @classmethod
    def class_name(cls) -> str:
        return "MarkdownElementNodeParser"

    def get_nodes_from_node(self, node: TextNode) -> List[BaseNode]:
        """Get nodes from node."""
        elements = self.extract_elements(
            node.get_content(), table_filters=[self.filter_table]
        )
        table_elements = self.get_table_elements(elements)
        # extract summaries over table elements
        self.extract_table_summaries(table_elements)
        # convert into nodes
        # will return a list of Nodes and Index Nodes
        return self.get_nodes_from_elements(elements)

    def extract_elements(
        self, text: str, table_filters: Optional[List[Callable]] = None, **kwargs: Any
    ) -> List[Element]:
        """Extract elements from text."""
        lines = text.split("\n")
        currentElement = None

        elements: List[Element] = []
        # Then parse the lines
        for line in lines:
            if line.startswith("```"):
                # check if this is the end of a code block
                if currentElement is not None and currentElement.type == "code":
                    elements.append(currentElement)
                    currentElement = None
                    # if there is some text after the ``` create a text element with it
                    if len(line) > 3:
                        elements.append(
                            Element(
                                id=f"id_{len(elements)}",
                                type="text",
                                element=line.lstrip("```"),
                            )
                        )

                elif line.count("```") == 2 and line[-3] != "`":
                    # check if inline code block (aka have a second ``` in line but not at the end)
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}",
                        type="code",
                        element=line.lstrip("```"),
                    )
                elif currentElement is not None and currentElement.type == "text":
                    currentElement.element += "\n" + line
                else:
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="text", element=line
                    )

            elif currentElement is not None and currentElement.type == "code":
                currentElement.element += "\n" + line

            elif line.startswith("|"):
                if currentElement is not None and currentElement.type != "table":
                    if currentElement is not None:
                        elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="table", element=line
                    )
                elif currentElement is not None:
                    currentElement.element += "\n" + line
                else:
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="table", element=line
                    )
            elif line.startswith("#"):
                if currentElement is not None:
                    elements.append(currentElement)
                currentElement = Element(
                    id=f"id_{len(elements)}",
                    type="title",
                    element=line.lstrip("#"),
                    title_level=len(line) - len(line.lstrip("#")),
                )
            else:
                if currentElement is not None and currentElement.type != "text":
                    elements.append(currentElement)
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="text", element=line
                    )
                elif currentElement is not None:
                    currentElement.element += "\n" + line
                else:
                    currentElement = Element(
                        id=f"id_{len(elements)}", type="text", element=line
                    )
        if currentElement is not None:
            elements.append(currentElement)

        for idx, element in enumerate(elements):
            if element.type == "table":
                if table_filters is not None:
                    should_keep = all(tf(element) for tf in table_filters)
                else:
                    should_keep = True  # default to keeping all tables
                # if the element is a table, convert it to a dataframe
                if should_keep:
                    table = md_to_df(element.element)
                    elements[idx] = Element(
                        id=f"id_{idx}", type="table", element=element, table=table
                    )
                else:
                    elements[idx] = Element(
                        id=f"id_{idx}",
                        type="text",
                        element=element.element,
                    )
            else:
                # if the element is not a table, keep it as to text
                elements[idx] = Element(
                    id=f"id_{idx}",
                    type="text",
                    element=element.element,
                )

        # merge consecutive text elements together for now
        merged_elements: List[Element] = []
        for element in elements:
            if (
                len(merged_elements) > 0
                and element.type == "text"
                and merged_elements[-1].type == "text"
            ):
                merged_elements[-1].element += "\n" + element.element
            else:
                merged_elements.append(element)
        elements = merged_elements
        return merged_elements

    def filter_table(self, table_element: Any) -> bool:
        """Filter tables."""
        table_df = md_to_df(table_element.element)

        # check if table_df is not None, has more than one row, and more than one column
        return table_df is not None and not table_df.empty and len(table_df.columns) > 1