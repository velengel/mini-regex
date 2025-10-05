# matchbox

A tiny regular expression evaluator based on Abstract Syntax Tree (AST) in Python.

This project provides a simple regex engine that first parses a regular expression into an AST and then evaluates it against a given text.

---

## Supported Syntax

-   `.` : Any single character
-   `*` : Zero or more repetitions of the preceding character
-   `+` : One or more repetitions of the preceding character
-   `?` : Zero or one repetition of the preceding character
-   `|` : Alternation (OR)
-   `()`: Grouping
-   `^` : Start of the string anchor
-   `$` : End of the string anchor

---

## How to Run

### 1. Command Line Interface (Recommended)

You can execute the regex match from the command line using the `matchbox` module. It supports both full matching and searching.

```bash
# Full match (the entire text must match the pattern)
python -m matchbox <pattern> <text>

# Search (find a substring that matches the pattern)
python -m matchbox <pattern> <text> --search
```

**Examples:**

```bash
# Full match
python -m matchbox "a(b|c)*d" "acccbd"
# ✅ Matched

# Search
python -m matchbox "a*b" "xxaaabyy" --search
# ✅ Matched
```

#### Tracing the Evaluation

Use the `--trace` option to visualize the backtracking process of the AST evaluator. This is useful for debugging your patterns. The output is colorized using the `rich` library.

```bash
python -m matchbox "a(b|c)d" "acd" --trace
```

### 2. Interactive Mode

You can also run an interactive prompt.

```bash
python main.py
```

**Example:**

```
Mini Regex Engine (matchbox)
Enter regex: a*b
Enter text: aaab
✅ MATCH!
```

---

## Key Concepts

This regex engine is composed of three main components:

1.  **Lexer (`lexer.py`)**:
    The lexer takes a regular expression string and breaks it down into a sequence of tokens (e.g., `CHAR`, `*`, `|`).

2.  **Parser (`parser.py`)**:
    The parser consumes the token stream from the lexer and builds an Abstract Syntax Tree (AST). The nodes of this tree (`ast_nodes.py`) represent the structure of the regular expression (e.g., `ConcatNode`, `OrNode`, `RepeatNode`).

3.  **Evaluator (`evaluator.py`)**:
    The evaluator traverses the AST to determine if the pattern matches the input text. The `fullmatch` and `search` functions are the entry points, which recursively call the `match` method on each node. This AST-based approach allows for handling complex nested structures and provides clear evaluation paths, which can be traced for debugging.

---

## Directory Structure

```
mini-regex/
├── main.py               # Entry point for interactive mode
├── requirements.txt      # Dependencies
├── matchbox/
│   ├── __main__.py       # Entry point for CLI mode
│   ├── lexer.py          # Lexical analysis
│   ├── parser.py         # AST construction
│   ├── ast_nodes.py      # AST node definitions
│   └── evaluator.py      # AST-based regex evaluation
└── tests/
    ├── test_evaluator.py # Tests for the AST-based evaluator
    ├── test_parser.py    # Tests for the parser
    └── test_matchbox.py  # Legacy tests (can be merged or removed)
```

---

## How to Test

To run the test suite, install the dependencies and run `pytest`.

```bash
pip install -r requirements.txt
pytest
```

---

## Code Quality

This project uses `black` for code formatting and `ruff` for linting to ensure code quality and consistency.

### Running Manually

```bash
# Format code with black
.venv/bin/black .

# Lint and auto-fix with ruff
.venv/bin/ruff check --fix .
```

### Configuration

Currently, both tools run with their default settings as there is no specific configuration file.

To customize their behavior, you can create a `pyproject.toml` file in the project root. For example:

```toml
# pyproject.toml

[tool.black]
line-length = 88

[tool.ruff]
line-length = 88
select = ["E", "F", "I"] # Enable specific linting rules
```