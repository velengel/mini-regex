from dataclasses import dataclass
from rich.console import Console

console = Console()


@dataclass
class MatchContext:
    """マッチング処理中に引き回すコンテキスト情報"""

    text: str  # 現在のマッチング対象テキスト
    original_text: str  # 元の完全なテキスト
    trace: bool = False
    depth: int = 0

    def advance(self, n=1):
        """テキストをn文字進めた新しいコンテキストを返す"""
        return MatchContext(
            text=self.text[n:],
            original_text=self.original_text,
            trace=self.trace,
            depth=self.depth + 1,
        )

    def next_depth(self):
        return MatchContext(
            text=self.text,
            original_text=self.original_text,
            trace=self.trace,
            depth=self.depth + 1,
        )


class Node:
    """ASTノードの基底クラス"""

    def match(self, ctx: MatchContext):
        raise NotImplementedError


# ----------------------------------------------------------------------
# アンカー (^, $)
# ----------------------------------------------------------------------
class AnchorNode(Node):
    def __init__(self, anchor_type):
        if anchor_type not in ("^", "$"):
            raise ValueError(f"Invalid anchor type: {anchor_type}")
        self.anchor_type = anchor_type

    def match(self, ctx: MatchContext):
        pad = "  " * ctx.depth
        if ctx.trace:
            console.print(
                f"{pad}[blue][Anchor('{self.anchor_type}')][/blue] text='[dim]{ctx.text}[/dim]'"
            )

        # アンカーは文字を消費しない
        if self.anchor_type == "^" and ctx.text == ctx.original_text:
            if ctx.trace:
                console.print(f"{pad}[green]✔️ Anchor start matches[/green]")
            return [ctx.text]  # 成功、テキストはそのまま
        elif self.anchor_type == "$" and ctx.text == "":
            if ctx.trace:
                console.print(f"{pad}[green]✔️ Anchor end matches[/green]")
            return [ctx.text]
        else:
            if ctx.trace:
                console.print(f"{pad}[red]❌ FAIL (Anchor condition not met)[/red]")
            return None

    def __repr__(self):
        return f"Anchor({self.anchor_type!r})"


# ----------------------------------------------------------------------
# リテラル文字
# ----------------------------------------------------------------------
class CharNode(Node):
    def __init__(self, char):
        self.char = char

    def match(self, ctx: MatchContext):
        pad = "  " * ctx.depth
        if ctx.trace:
            console.print(
                f"{pad}[blue][Char('{self.char}')][/blue] text='[dim]{ctx.text}[/dim]'"
            )

        if not ctx.text:
            if ctx.trace:
                console.print(f"{pad}[red]❌ FAIL (no input)[/red]")
            return None

        if self.char == "." or ctx.text[0] == self.char:
            if ctx.trace:
                console.print(
                    f"{pad}[yellow]→ consumes '{ctx.text[0]}'[/yellow] -> rest='[dim]{ctx.text[1:]}[/dim]'"
                )
            return [ctx.text[1:]]
        else:
            if ctx.trace:
                console.print(
                    f"{pad}[red]❌ FAIL (expected '{self.char}', got '{ctx.text[0]}')[/red]"
                )
            return None

    def __repr__(self):
        return f"Char({self.char!r})"


# ----------------------------------------------------------------------
# 繰り返し (*, +, ?)
# ----------------------------------------------------------------------
class RepeatNode(Node):
    def __init__(self, node, op):
        self.node = node
        self.op = op

    def match(self, ctx: MatchContext):
        pad = "  " * ctx.depth
        if ctx.trace:
            console.print(
                f"{pad}[blue][Repeat {self.op}][/blue] start text='[dim]{ctx.text}[/dim]'"
            )

        results = [ctx.text]
        current = [ctx.text]

        while current:
            new = []
            for t in current:
                nexts = self.node.match(ctx.next_depth().advance(len(ctx.text) - len(t)))
                if nexts:
                    for n in nexts:
                        if n not in results:
                            results.append(n)
                            new.append(n)
            current = new

        # 演算子別の調整
        if self.op == "+":
            results = results[1:] if len(results) > 1 else []
        elif self.op == "?":
            results = results[:2]

        if ctx.trace:
            for r in results:
                console.print(
                    f"{pad}[green]✔️ Repeat result rest='[dim]{r}[/dim]'[/green]"
                )

        return results if results else None

    def __repr__(self):
        return f"Repeat({self.node}, {self.op!r})"


# ----------------------------------------------------------------------
# 連結 (ab)
# ----------------------------------------------------------------------
class ConcatNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def match(self, ctx: MatchContext):
        pad = "  " * ctx.depth
        if ctx.trace:
            console.print(f"{pad}[blue][Concat][/blue] start text='[dim]{ctx.text}[/dim]'")

        left_res = self.left.match(ctx.next_depth())
        results = []
        if left_res:
            for rem in left_res:
                new_ctx = ctx.next_depth().advance(len(ctx.text) - len(rem))
                right_res = self.right.match(new_ctx)
                if right_res:
                    results.extend(right_res)

        if ctx.trace:
            for r in results:
                console.print(
                    f"{pad}[green]✔️ Concat result rest='[dim]{r}[/dim]'[/green]"
                )

        return results if results else None

    def __repr__(self):
        return f"Concat({self.left}, {self.right})"


# ----------------------------------------------------------------------
# OR (a|b)
# ----------------------------------------------------------------------
class OrNode(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def match(self, ctx: MatchContext):
        pad = "  " * ctx.depth
        if ctx.trace:
            console.print(f"{pad}[blue][Or][/blue] start text='[dim]{ctx.text}[/dim]'")

        left_res = self.left.match(ctx.next_depth())
        right_res = self.right.match(ctx.next_depth())

        results = []
        if left_res:
            results.extend(left_res)
        if right_res:
            results.extend(right_res)

        if ctx.trace:
            for r in results:
                console.print(f"{pad}[green]✔️ Or result rest='[dim]{r}[/dim]'[/green]")

        return results if results else None

    def __repr__(self):
        return f"Or({self.left}, {self.right})"