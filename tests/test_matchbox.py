from matchbox.evaluator import fullmatch, search


def test_basic():
    assert fullmatch("a", "a")
    assert not fullmatch("a", "b")


def test_dot_and_anchor():
    assert fullmatch(".", "x")
    assert not fullmatch(".", "")
    assert fullmatch("a*b", "aaab")


def test_plus_and_question():
    assert fullmatch("a+", "a")
    assert fullmatch("a+", "aaaa")
    assert not fullmatch("a+", "")
    assert fullmatch("a?", "")
    assert fullmatch("a?", "a")
    assert not fullmatch("a?", "aa")


def test_or_operator():
    assert fullmatch("a|b", "a")
    assert fullmatch("a|b", "b")
    assert not fullmatch("a|b", "c")


# ✅ 部分一致（search）テストを追加
def test_search_partial_match():
    # 部分一致あり
    assert search("a*b", "xxaaabyy")  # "aaab" にマッチ
    assert search("abc", "123abc456")  # 中間に出現
    assert search("x+", "abxxxcd")  # 連続x
    # 全体一致も当然通る
    assert search("a*b", "aaab")
    # 一致しないケース
    assert not search("xyz", "abcde")
    assert not search("a+b", "ccc")
