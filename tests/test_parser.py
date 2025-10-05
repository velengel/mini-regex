from matchbox.parser import parse
from matchbox.ast_nodes import CharNode, RepeatNode, ConcatNode, OrNode


def test_simple_char():
    ast = parse("a")
    assert isinstance(ast, CharNode)
    assert ast.char == "a"


def test_repeat_and_or():
    ast = parse("a|b*")
    assert isinstance(ast, OrNode)
    assert isinstance(ast.left, CharNode)
    assert isinstance(ast.right, RepeatNode)
    assert ast.right.op == "*"
    assert ast.right.node.char == "b"


def test_concat_group():
    ast = parse("(ab)+c")
    assert isinstance(ast, ConcatNode)
    assert isinstance(ast.left, RepeatNode)
    assert isinstance(ast.left.node, ConcatNode)
    assert isinstance(ast.right, CharNode)
    assert ast.right.char == "c"
