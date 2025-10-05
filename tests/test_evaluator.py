from matchbox.evaluator import fullmatch


def test_basic_literals():
    assert fullmatch("a", "a")
    assert not fullmatch("a", "b")


def test_or():
    assert fullmatch("a|b", "a")
    assert fullmatch("a|b", "b")
    assert not fullmatch("a|b", "c")


def test_concat():
    assert fullmatch("ab", "ab")
    assert not fullmatch("ab", "a")


def test_repeat():
    assert fullmatch("a*", "")
    assert fullmatch("a*", "aaaa")
    assert fullmatch("a+", "a")
    assert not fullmatch("a+", "")
    assert fullmatch("a?", "")
    assert fullmatch("a?", "a")
    assert not fullmatch("a?", "aa")
