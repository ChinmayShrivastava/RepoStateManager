# TODO

1. Extract Table headings
2. Add the metadata about the table to the root node of the table - table name, number of rows and cols
3. Generate the explanations for semantic search

4. Chunk the PDFs
5. For each chunk (including the table node) add document identifier (different fron Node UID)
6. A document identifier is a unique string of characters that makes the chunk searchable inside the doument, e.g. table 1.1, etc

7. Add interconnections between these chunks where these chunks are called using their document identifiers
8. Generate explanations for vector search and attach sufficient metadata to each vector such that the vector space is searchable with metadata filtering for increased flexibility