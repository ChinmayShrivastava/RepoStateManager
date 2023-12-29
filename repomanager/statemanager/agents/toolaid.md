# This is a non-exhaustive list of the specific retrieval tools we need to create and functions for these tools that we need to implement to make the returned context very specific and reduce the amount of it that is returned.

1. class->init attributes
2. class->methods (sync)
    * Means the class's methods + the parent class's methods
3. class->methods (async)
    * Means the class's methods + the parent class's methods
4. class->code (minimal) - this might need to be even shorter. How can we abstract away most of the code?
5. class method code - need to make sure which code to reference, the class's or the parent class's
6. 

**Perform Vector and Fuzzy Search Wherever Possible**

## Here is a high level view of the potential (some are already coded and available) tools

1. `The schema tool` - takes in a node type or a node name (basically some identifier for the node), and returns the meta schema information on the types of edges that it has (incoming and outgoing).
2. `The node tool` - takes in a unique node identifier (name), and some relevant context, based on which it runs very specific pipelines to retrieve information related to the code which it then returns.
3. `The human to tech breaker` - an agent/completion that takes in the human query and breaks it into sub-queries to retreive information on each independently and then (maybe) extracts insights from it to pass it into the final prompt.
4. `The semantic response finder` - For very vague queries, not specifying any relevant node name, this tool will run vector search to find the relevant node.
5. 