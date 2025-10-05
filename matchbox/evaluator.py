from matchbox.parser import parse
from rich.console import Console

console = Console()


def fullmatch(pattern: str, text: str, trace=False) -> bool:
    """テキスト全体が正規表現に一致するか"""
    ast = parse(pattern)
    if trace:
        console.rule(f"[bold cyan]TRACE for /{pattern}/ on '{text}'[/]")
    result = ast.match(text, trace=trace, depth=0)
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
    for i in range(len(text)):
        sub = text[i:]
        if trace:
            console.rule(f"[bold cyan]TRY at index {i} — '{sub}'[/]")
        result = ast.match(sub, trace=trace, depth=0)
        # ✅ 残りが空("")でなくても、マッチしていればOKにする
        if result:
            if trace:
                console.print(f"[green]✅ SUCCESS at index {i}[/green]")
            return True
    if trace:
        console.print("[red]❌ No partial match found[/red]")
    return False
