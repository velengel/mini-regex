# matchbox/lexer.py
from dataclasses import dataclass


@dataclass
class Token:
    type: str
    value: str = ""


def tokenize(pattern: str):
    tokens = []
    specials = {"*", "+", "?", "|", "(", ")", ".", "^", "$"}
    for ch in pattern:
        if ch in specials:
            tokens.append(Token(ch))
        else:
            tokens.append(Token("CHAR", ch))
    return tokens
