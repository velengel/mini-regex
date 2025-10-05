# matchbox/__main__.py
import argparse
from matchbox.evaluator import fullmatch, search


def main():
    parser = argparse.ArgumentParser(description="Mini regex matcher (AST-based)")
    parser.add_argument("pattern", help="正規表現パターン")
    parser.add_argument("text", help="テキスト文字列")
    parser.add_argument(
        "--trace", action="store_true", help="バックトラッキングの経路を表示"
    )
    parser.add_argument("--search", action="store_true", help="部分一致モード")
    args = parser.parse_args()

    if args.search:
        success = search(args.pattern, args.text, trace=args.trace)
    else:
        success = fullmatch(args.pattern, args.text, trace=args.trace)

    if success:
        print("✅  Matched")
    else:
        print("❌  Not matched")


if __name__ == "__main__":
    main()
