from rich.console import Console

console = Console()


class Node:
    """ASTノードの基底クラス"""

    def match(self, text, trace=False, depth=0):
        raise NotImplementedError


# ----------------------------------------------------------------------
# リテラル文字
# ----------------------------------------------------------------------
class CharNode(Node):
    def __init__(self, char):
        self.char = char

    def match(self, text, trace=False, depth=0):
        pad = "  " * depth
        if trace:
            console.print(
                f"{pad}[blue][Char('{self.char}')][/blue] text='[dim]{text}[/dim]'"
            )

        if not text:
            if trace:
                console.print(f"{pad}[red]❌ FAIL (no input)[/red]")
            return None

        if self.char == "." or text[0] == self.char:
            if trace:
                console.print(
                    f"{pad}[yellow]→ consumes '{text[0]}'[/yellow] -> rest='[dim]{text[1:]}[/dim]'"
                )
            return [text[1:]]
        else:
            if trace:
                console.print(
                    f"{pad}[red]❌ FAIL (expected '{self.char}', got '{text[0]}')[/red]"
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

    def match(self, text, trace=False, depth=0):
        pad = "  " * depth
        if trace:
            console.print(
                f"{pad}[blue][Repeat {self.op}][/blue] start text='[dim]{text}[/dim]'"
            )

        results = [text]
        current = [text]

        while current:
            new = []
            for t in current:
                nexts = self.node.match(t, trace, depth + 1)
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

        if trace:
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

    def match(self, text, trace=False, depth=0):
        pad = "  " * depth
        if trace:
            console.print(f"{pad}[blue][Concat][/blue] start text='[dim]{text}[/dim]'")

        left_res = self.left.match(text, trace, depth + 1)
        results = []
        if left_res:
            for rem in left_res:
                right_res = self.right.match(rem, trace, depth + 1)
                if right_res:
                    results.extend(right_res)

        if trace:
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

    def match(self, text, trace=False, depth=0):
        pad = "  " * depth
        if trace:
            console.print(f"{pad}[blue][Or][/blue] start text='[dim]{text}[/dim]'")

        left_res = self.left.match(text, trace, depth + 1)
        right_res = self.right.match(text, trace, depth + 1)

        results = []
        if left_res:
            results.extend(left_res)
        if right_res:
            results.extend(right_res)

        if trace:
            for r in results:
                console.print(f"{pad}[green]✔️ Or result rest='[dim]{r}[/dim]'[/green]")

        return results if results else None

    def __repr__(self):
        return f"Or({self.left}, {self.right})"
