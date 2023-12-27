def test_tsx_code_splitter() -> None:
    """Test case for code splitting using typescript."""
    if "CI" in os.environ:
        return

    code_splitter = CodeSplitter(
        language="typescript", chunk_lines=4, chunk_lines_overlap=1, max_chars=50
    )

    text = """\
import React from 'react';

interface Person {
  name: string;
  age: number;
}

const ExampleComponent: React.FC = () => {
  const person: Person = {
    name: 'John Doe',
    age: 30,
  };

  return (
    <div>
      <h1>Hello, {person.name}!</h1>
      <p>You are {person.age} years old.</p>
    </div>
  );
};

export default ExampleComponent;"""

    chunks = code_splitter.split_text(text)
    assert chunks[0].startswith("import React from 'react';")
    assert chunks[1].startswith("interface Person")
