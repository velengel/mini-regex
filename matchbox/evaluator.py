from matchbox.parser import parse
from matchbox.ast_nodes import MatchContext
from rich.console import Console

console = Console()


def fullmatch(pattern: str, text: str, trace=False) -> bool:
    """テキスト全体が正規表現に一致するか"""
    ast = parse(pattern)
    ctx = MatchContext(text=text, original_text=text, trace=trace)
    if trace:
        console.rule(f"[bold cyan]TRACE for /{pattern}/ on '{text}' (fullmatch)[/]")
    result = ast.match(ctx)
    success = result is not None and "" in result
    if trace:
        if success:
            console.print("[bold green]✅ SUCCESS[/bold green]")
        else:
            console.print("[bold red]❌ FAIL[/bold red]")
    return success


def search(pattern: str, text: str, trace=False) -> bool:
    """テキストのどこか一部に正規表現が一致するか"""
    ast = parse(pattern)
    for i in range(len(text) + 1):
        sub = text[i:]
        ctx = MatchContext(text=sub, original_text=text, trace=trace)
        if trace:
            console.rule(f"[bold cyan]TRY at index {i} — '{sub}'[/]")
        result = ast.match(ctx)
        # ✅ 残りが空("")でなくても、マッチしていればOKにする
        if result is not None:
            if trace:
                console.print(f"[green]✅ SUCCESS at index {i}[/green]")
            return True
    if trace:
        console.print("[red]❌ No partial match found[/red]")
    return False
