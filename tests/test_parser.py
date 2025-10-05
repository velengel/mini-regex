import pytest
from matchbox.parser import parse
from matchbox.ast_nodes import CharNode, RepeatNode, ConcatNode, OrNode, AnchorNode


def test_simple_char():
    ast = parse("a")
    assert isinstance(ast, CharNode)
    assert ast.char == "a"


def test_dot():
    ast = parse(".")
    assert isinstance(ast, CharNode)
    assert ast.char == "."


def test_repeat_and_or():
    ast = parse("a|b*")
    assert isinstance(ast, OrNode)
    assert isinstance(ast.left, CharNode)
    assert ast.left.char == "a"
    assert isinstance(ast.right, RepeatNode)
    assert ast.right.op == "*"
    assert isinstance(ast.right.node, CharNode)
    assert ast.right.node.char == "b"


def test_concat_group():
    ast = parse("(ab)+c")
    assert isinstance(ast, ConcatNode)
    assert isinstance(ast.left, RepeatNode)
    assert ast.left.op == "+"
    assert isinstance(ast.left.node, ConcatNode)
    assert isinstance(ast.right, CharNode)
    assert ast.right.char == "c"


def test_deeply_nested_groups():
    # Simply test that parsing complex nested patterns doesn't crash
    # and produces a non-null AST.
    try:
        ast = parse("a(b(c|d)*e)f")
        assert ast is not None
        assert isinstance(ast, ConcatNode)
    except Exception as e:
        pytest.fail(f"Parsing deeply nested group failed: {e}")


def test_anchors_parsing():
    # Start anchor
    ast_start = parse("^a")
    assert isinstance(ast_start, ConcatNode)
    assert isinstance(ast_start.left, AnchorNode)
    assert ast_start.left.anchor_type == "^"
    assert isinstance(ast_start.right, CharNode)

    # End anchor
    ast_end = parse("a$")
    assert isinstance(ast_end, ConcatNode)
    assert isinstance(ast_end.left, CharNode)
    assert isinstance(ast_end.right, AnchorNode)
    assert ast_end.right.anchor_type == "$"

    # Both anchors
    ast_both = parse("^a$")
    assert isinstance(ast_both, ConcatNode)
    assert isinstance(ast_both.left, ConcatNode)
    assert isinstance(ast_both.left.left, AnchorNode)
    assert isinstance(ast_both.left.right, CharNode)
    assert isinstance(ast_both.right, AnchorNode)

    # Just anchors
    ast_just_anchors = parse("^$")
    assert isinstance(ast_just_anchors, ConcatNode)
    assert isinstance(ast_just_anchors.left, AnchorNode)
    assert isinstance(ast_just_anchors.right, AnchorNode)


@pytest.mark.parametrize(
    "pattern",
    [
        "*a",
        "+a",
        "?a",
        "a|",
        "|a",
        "(a|b",
        "a)b",
        "a((b)",
        "a**",
        "^a^",  # Invalid anchor position
        "a$b",  # Invalid anchor position
    ],
)
def test_invalid_syntax(pattern):
    with pytest.raises(SyntaxError):
        parse(pattern)
