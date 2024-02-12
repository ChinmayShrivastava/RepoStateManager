# TODO: might later want to add more general examples
DEFAULT_EXTRACT_UNIQUE_IDENTIFIERS = """Given an excerpt from a pdf, give a tuple of unique identifiers, if any.
----------
Example 1:
Input:
2.3.3.3 Spacing of Ceiling-Level Storage Sprinklers
2.3.3.3.1 Install ceiling-level Storage sprinklers under unobstructed ceiling construction in accordance with
the linear and area spacing guidelines in Table 1.
Output:
(2.3.3.3, 2.3.3.3.1)
Example 2:
Input:
Table 1. Spacing of Ceiling-Level Storage Sprinklers Under Unobstructed Ceiling Construction
Output:
(table 1,)
Example 3:
Input:
Extend the hydraulic design for storage occupancies at least 15 ft (4.5 m) beyond all edges of the storage,
or to a wall, whenever there is mixed-use occupancy.
Output:
()
---
Input:
{text}
Output:"""

# TODO: This is getting quite expensive, code a way to identify the unique identifiers without using the API. Maybe use regex? But with regex, certain identifiers might be missed.
DEFAULT_EXTRACT_CITATIONS = """Given an excerpt from a pdf, return an exhaustive list of tuples containing elements that connect to each other by citation. The format should be, (referee, referred). Use the unique identifiers (i.e. the section numbers, table numbers, etc.).
----------
Example 1:
Input:
2.3.3.3 Spacing of Ceiling-Level Storage Sprinklers
2.3.3.3.1 Install ceiling-level Storage sprinklers under unobstructed ceiling construction in accordance with
the linear and area spacing guidelines in Tables 1 and 2.
Output:
[(2.3.3.3.1, table 1),(2.3.3.3.1, table 2)]
Example 2:
Input:
2.3.3.1.1 See Section 2.3.3.7 for the protection design guidelines of ceiling-level Storage sprinklers. Tables
2 through 6 provide design guidelines for solid-piled, palletized, shelf, and bin-box storage arrangements.
Output:
[(2.3.3.1.1, 2.3.3.7),(2.3.3.1.1, table 2),(2.3.3.1.1, table 3),(2.3.3.1.1, table 4),(2.3.3.1.1, table 5),(2.3.3.1.1, table 6),]
----------
Input:
{text}
Output:"""


# TODO: This is good, but can be better. Also add the functionality for when there are no identifiers. This is true for most of the pdfs. 89 is an exception, where there are a lot of identifiers.
DEFAULT_EXTRACT_INSIGHTS = """Given an excerpt from a pdf, extract independent insights and attach it to the unique identifier it refers to (i.e. the section numbers, table numbers, etc.). Return list of tuples of the type (unique identifier, insight). A unique identifier can have multiple insights.

The insights should be in a simplified, more accessible tone.
----------
Example 1:
Input:
2.3.3.3 Spacing of Ceiling-Level Storage Sprinklers
2.3.3.3.1 Install ceiling-level Storage sprinklers under unobstructed ceiling construction in accordance with
the linear and area spacing guidelines in Table 1.
Output:
[(2.3.3.3, contains information on spacing of ceiling level storage sprinklers),(2.3.3.3.1, ceiling level storage sprinklers under unobstructed ceiling construction should be installed in accordance to table 1)]
Example 2:
Input:
2.3.3.1.1 See Section 2.3.3.7 for the protection design guidelines of ceiling-level Storage sprinklers. Tables
2 through 6 provide design guidelines for solid-piled, palletized, shelf, and bin-box storage arrangements.
Output:
[(2.3.3.1.1, tables 2 through 6 provide design guidelines for solid-piled, palletized, shelf, and bin-box storage arrangements)]
----------
Input:
{text}
Output:"""