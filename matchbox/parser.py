# matchbox/parser.py
from matchbox.lexer import tokenize
from matchbox.ast_nodes import CharNode, RepeatNode, ConcatNode, OrNode


def parse(pattern: str):
    tokens = tokenize(pattern)
    pos = 0

    def peek():
        return tokens[pos] if pos < len(tokens) else None

    def consume():
        nonlocal pos
        t = tokens[pos]
        pos += 1
        return t

    def parse_atom():
        tok = consume()
        if tok.type == "CHAR":
            node = CharNode(tok.value)
        elif tok.type == ".":
            node = CharNode(".")
        elif tok.type == "(":
            node = parse_expr()
            assert consume().type == ")", "missing ')'"
        else:
            raise SyntaxError(f"Unexpected token: {tok}")
        # 繰り返し演算子処理
        if peek() and peek().type in {"*", "+", "?"}:
            op = consume().type
            node = RepeatNode(node, op)
        return node

    def parse_concat():
        node = parse_atom()
        while peek() and peek().type not in {"|", ")"}:
            node = ConcatNode(node, parse_atom())
        return node

    def parse_expr():
        node = parse_concat()
        while peek() and peek().type == "|":
            consume()
            node = OrNode(node, parse_concat())
        return node

    ast = parse_expr()
    if pos != len(tokens):
        raise SyntaxError("Extra tokens after parse")
    return ast
