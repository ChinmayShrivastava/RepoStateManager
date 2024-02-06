from pydantic import BaseModel

class Node(BaseModel):
    name: str
    type: str
    file_name: str
    # optional fields
    code: str = None
    code_start_line: int = None
    code_end_line: int = None