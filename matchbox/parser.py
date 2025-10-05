# matchbox/parser.py
from matchbox.lexer import tokenize
from matchbox.ast_nodes import CharNode, RepeatNode, ConcatNode, OrNode, AnchorNode


def parse(pattern: str):
    tokens = tokenize(pattern)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume(expected_type=None):
        nonlocal pos
        if not peek():
            if expected_type:
                raise SyntaxError(f"Expected {expected_type} but found end of pattern")
            else:
                raise SyntaxError("Unexpected end of pattern")
        if expected_type and peek().type != expected_type:
            raise SyntaxError(f"Expected {expected_type} but found {peek().type}")
        t = tokens[pos]
        pos += 1
        return t

    def parse_atom():
        if not peek() or peek().type in {"|", ")"}:
            raise SyntaxError("Pattern cannot start with or be empty inside a group")

        tok = peek()
        if tok.type == "CHAR" or tok.type == ".":
            consume()
            node = CharNode(tok.value or tok.type)
        elif tok.type == "(":
            consume("(")
            node = parse_expr()
            consume(")")
        else:
            raise SyntaxError(f"Unexpected token: {tok}")

        if peek() and peek().type in {"*", "+", "?"}:
            op = consume().type
            if isinstance(node, RepeatNode):
                raise SyntaxError("Multiple repeaters for the same atom")
            node = RepeatNode(node, op)
        return node

    def parse_concat():
        if not peek() or peek().type in {"|", ")", "*", "+", "?"}:
            raise SyntaxError(
                f"Unexpected start of sub-expression: {peek().type if peek() else 'None'}"
            )

        node = parse_atom()
        while peek() and peek().type not in {"|", ")", "$"}:
            node = ConcatNode(node, parse_atom())
        return node

    def parse_expr():
        node = parse_concat()
        while peek() and peek().type == "|":
            consume("|")
            if not peek() or peek().type == ")":
                raise SyntaxError("Dangling alternator '|'")
            node = OrNode(node, parse_concat())
        return node

    def parse_toplevel():
        # Toplevel parsing handles optional anchors
        nodes = []
        if peek() and peek().type == "^":
            nodes.append(AnchorNode(consume().type))

        if peek() and peek().type != "$":  # Don't parse if it's just `^$`
            nodes.append(parse_expr())

        if peek() and peek().type == "$":
            nodes.append(AnchorNode(consume().type))

        if not nodes:
            raise SyntaxError("Pattern cannot be empty")

        # Build a single ConcatNode from the list of nodes
        if len(nodes) == 1:
            return nodes[0]
        else:
            ast = nodes[0]
            for node in nodes[1:]:
                ast = ConcatNode(ast, node)
            return ast

    if not tokens:
        return CharNode("")  # Match empty string for empty pattern

    ast = parse_toplevel()
    if pos != len(tokens):
        raise SyntaxError(
            f"Extra tokens after parse: {"".join(t.value for t in tokens[pos:])}"
        )
    return ast
