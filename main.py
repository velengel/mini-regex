from matchbox.evaluator import fullmatch


def main():
    print("Mini Regex Engine (matchbox)")
    regex = input("Enter regex: ")
    text = input("Enter text: ")

    result = fullmatch(regex, text)
    print("✅ MATCH!" if result else "❌ NO MATCH")


if __name__ == "__main__":
    main()
