import pytest
from matchbox.evaluator import fullmatch, search


# --- fullmatch tests ---


def test_basic_literals():
    assert fullmatch("a", "a")
    assert not fullmatch("a", "b")
    assert fullmatch("abc", "abc")
    assert not fullmatch("abc", "abd")


def test_dot():
    assert fullmatch(".", "a")
    assert fullmatch(".", "Z")
    assert fullmatch("a.c", "abc")
    assert not fullmatch(".", "")


def test_or():
    assert fullmatch("a|b", "a")
    assert fullmatch("a|b", "b")
    assert not fullmatch("a|b", "c")
    assert fullmatch("ab|cd", "ab")
    assert fullmatch("ab|cd", "cd")
    assert not fullmatch("ab|cd", "ac")


def test_concat():
    assert fullmatch("ab", "ab")
    assert not fullmatch("ab", "a")


@pytest.mark.parametrize(
    "pattern, text, expected",
    [
        # Star (*)
        ("a*", "", True),
        ("a*", "aaaa", True),
        ("a*b", "b", True),
        ("a*b", "aaab", True),
        ("a*b", "aaac", False),
        (".*", "abcdef", True),
        # Plus (+)
        ("a+", "a", True),
        ("a+", "aaaa", True),
        ("a+", "", False),
        ("a+b", "ab", True),
        ("a+b", "aaab", True),
        ("a+b", "b", False),
        # Question (?)
        ("a?", "", True),
        ("a?", "a", True),
        ("a?", "aa", False),
        ("a?b", "b", True),
        ("a?b", "ab", True),
        ("a?b", "aab", False),
    ],
)
def test_repeaters(pattern, text, expected):
    assert fullmatch(pattern, text) == expected


@pytest.mark.parametrize(
    "pattern, text, expected",
    [
        # Anchors (^, $)
        ("^a", "a", True),
        ("^a", "abc", False), # fullmatch requires entire string
        ("c$", "c", True),
        ("c$", "abc", False), # fullmatch requires entire string
        ("^abc$", "abc", True),
        ("^abc$", "xabc", False),
        ("^abc$", "abcx", False),
        ("^$", "", True),
        ("^$", "a", False),
    ],
)
def test_anchors(pattern, text, expected):
    assert fullmatch(pattern, text) == expected


@pytest.mark.parametrize(
    "pattern, text, expected",
    [
        # Grouping and complex patterns
        ("a(b|c)d", "abd", True),
        ("a(b|c)d", "acd", True),
        ("a(b|c)d", "a_d", False),
        ("(ab)*", "ababab", True),
        ("(ab)*", "abababa", False),
        ("a(b|c)+d", "abcd", True),
        ("a(b|c)+d", "abccbd", True),
        ("a(b|c)+d", "ad", False),
    ],
)
def test_complex_patterns(pattern, text, expected):
    assert fullmatch(pattern, text) == expected


@pytest.mark.parametrize(
    "pattern, text, expected",
    [
        # Valid backtracking cases
        ("(a|aa)*c", "aaaaaac", True),
        ("(a|aa)*c", "aaaaaab", False),
    ],
)
def test_backtracking(pattern, text, expected):
    assert fullmatch(pattern, text) == expected


@pytest.mark.parametrize(
    "pattern",
    [
        "(a*)*c",  # multiple repeaters
        "(a+)?*",
    ],
)
def test_invalid_backtracking_patterns(pattern):
    """Test for patterns that should be rejected by the parser."""
    with pytest.raises(SyntaxError):
        # We only need to parse, not match
        from matchbox.parser import parse
        parse(pattern)


# --- search tests ---

@pytest.mark.parametrize(
    "pattern, text, expected",
    [
        ("b", "abc", True),  # Middle
        ("a", "abc", True),  # Start
        ("c", "abc", True),  # End
        ("x", "abc", False), # No match
        ("a*b", "xxaaabyy", True),
        ("a+b", "xxabyy", True),
        ("a+b", "xxbyy", False),
        (".*c", "ab_c_de", True),
        ("a(b|c)+d", "xx_acbd_yy", True),
        ("a(b|c)+d", "xx_ad_yy", False),
    ],
)
def test_search(pattern, text, expected):
    assert search(pattern, text) == expected