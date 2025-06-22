import sys
from typing import List
from enums import (
    TokenSpec,
    Token,
    TokenType,
    KEYWORDS,
    symbols,
    compound_ops,
    VIDEO_FUNCS,
)

class Lexer:
    def __init__(self, text: str) -> None:
        self.text = text
        self.pos = 0
        self.line = 1
        self.column = 1
        self.errors: List[str] = []

    def _peek(self) -> str:
        return self.text[self.pos] if self.pos < len(self.text) else ''

    def _advance(self) -> str:
        ch = self._peek()
        if ch:
            self.pos += 1
            if ch == '\n':
                self.line += 1
                self.column = 1
            else:
                self.column += 1
        return ch

    def _match(self, expected: str) -> bool:
        if self.text.startswith(expected, self.pos):
            for _ in expected:
                self._advance()
            return True
        return False

    def _skip_whitespace(self) -> None:
        while True:
            ch = self._peek()
            if ch == '':
                break
            if ch in ' \t\r\n':
                self._advance()
            else:
                break

    def _number(self) -> Token:
        start_pos = self.pos
        start_line = self.line
        start_col = self.column
        has_dot = False
        while True:
            ch = self._peek()
            if ch.isdigit():
                self._advance()
            elif ch == '.':
                if has_dot:
                    # malformed number like 1.2.3
                    while self._peek().isdigit() or self._peek() == '.':
                        self._advance()
                    lex = self.text[start_pos:self.pos]
                    self.errors.append(f"Malformed number '{lex}' at line {start_line}, column {start_col}")
                    return None
                has_dot = True
                self._advance()
            else:
                break

        lex = self.text[start_pos:self.pos]
        # identifier starting with digit
        nxt = self._peek()
        if nxt.isalpha() or nxt == '_':
            while self._peek().isalnum() or self._peek() == '_':
                self._advance()
            lex = self.text[start_pos:self.pos]
            self.errors.append(f"Invalid identifier '{lex}' at line {start_line}, column {start_col}")
            return None

        token_type = TokenType.FLOAT_LITERAL if has_dot else TokenType.INT_LITERAL
        return Token(token_type, lex, start_line, start_col)

    def _string(self) -> Token:
        start_line = self.line
        start_col = self.column
        start_index = self.pos
        self._advance()  # consume opening quote
        while True:
            ch = self._peek()
            if ch == '':
                self.errors.append(f"Unterminated string at line {start_line}, column {start_col}")
                return None
            if ch == '"':
                self._advance()  # consume closing quote
                lex = self.text[start_index:self.pos]
                return Token(TokenType.STRING_LITERAL, lex, start_line, start_col)
            if ch == '\n':
                self.errors.append(f"Unterminated string at line {start_line}, column {start_col}")
                return None
            self._advance()

    def _identifier(self) -> Token:
        start_pos = self.pos
        start_line = self.line
        start_col = self.column
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()
        lex = self.text[start_pos:self.pos]
        token_type = KEYWORDS.get(lex, TokenType.IDENTIFIER)
        return Token(token_type, lex, start_line, start_col)

    def _video_function(self) -> Token:
        start_line = self.line
        start_col = self.column
        self._advance()  # consume '@'
        if not (self._peek().isalpha() or self._peek() == '_'):
            invalid = '@' + self._peek()
            self.errors.append(
                f"Invalid character '{invalid}' at line {start_line}, column {start_col}"
            )
            if self._peek():
                self._advance()
            return None

        start = self.pos
        while self._peek().isalnum() or self._peek() == '_':
            self._advance()
        name = self.text[start:self.pos]
        lex = '@' + name
        token_type = VIDEO_FUNCS.get(lex)
        if token_type is None:
            self.errors.append(
                f"Invalid character '{lex}' at line {start_line}, column {start_col}"
            )
            return None
        return Token(token_type, lex, start_line, start_col)

    def tokenize(self) -> List[Token]:
        tokens: List[Token] = []
        while self.pos < len(self.text):
            self._skip_whitespace()
            if self.pos >= len(self.text):
                break

            ch = self._peek()
            start_line = self.line
            start_col = self.column

            if ch == '/' and self.text.startswith('//', self.pos):
                # skip comment
                while self._peek() and self._peek() != '\n':
                    self._advance()
                continue
            if ch == '/' and self.text.startswith('/*', self.pos):
                self.errors.append(f"Malformed comment at line {start_line}, column {start_col}")
                self._advance()
                self._advance()
                while self._peek():
                    if self.text.startswith('*/', self.pos):
                        self._advance()
                        self._advance()
                        break
                    if self._peek() == '\n':
                        break
                    self._advance()
                continue

            if ch.isdigit():
                tok = self._number()
                if tok:
                    tokens.append(tok)
                continue

            if ch == '"':
                tok = self._string()
                if tok:
                    tokens.append(tok)
                continue

            if ch.isalpha() or ch == '_':
                tok = self._identifier()
                if tok:
                    tokens.append(tok)
                continue

            if ch == '@':
                tok = self._video_function()
                if tok:
                    tokens.append(tok)
                continue

            # Compound operators
            two = self.text[self.pos:self.pos+2]
            if two in compound_ops:
                self._advance()
                self._advance()
                tokens.append(Token(compound_ops[two], two, start_line, start_col))
                continue

            # Single character tokens and operators
            if ch in symbols:
                self._advance()
                tokens.append(Token(symbols[ch], ch, start_line, start_col))
                continue
            if ch == '+':
                self._advance()
                # treat ++ as two plus tokens
                if self._peek() == '+':
                    tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
                    start_col = self.column
                    self._advance()
                    tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
                else:
                    tokens.append(Token(TokenType.PLUS, '+', start_line, start_col))
                continue
            if ch == '-':
                self._advance()
                tokens.append(Token(TokenType.MINUS, '-', start_line, start_col))
                continue
            if ch == '*':
                self._advance()
                tokens.append(Token(TokenType.MULT, '*', start_line, start_col))
                continue
            if ch == '/':
                self._advance()
                tokens.append(Token(TokenType.DIV, '/', start_line, start_col))
                continue
            if ch == '=':
                self._advance()
                tokens.append(Token(TokenType.ASSIGN, '=', start_line, start_col))
                continue
            if ch == '<':
                self._advance()
                tokens.append(Token(TokenType.LT, '<', start_line, start_col))
                continue
            if ch == '>':
                self._advance()
                tokens.append(Token(TokenType.GT, '>', start_line, start_col))
                continue
            if ch == '!':
                self._advance()
                tokens.append(Token(TokenType.ERROR, '!', start_line, start_col))
                self.errors.append(f"Invalid character '!' at line {start_line}, column {start_col}")
                continue

            # unrecognized character
            self.errors.append(f"Invalid character '{ch}' at line {start_line}, column {start_col}")
            self._advance()

        tokens.append(Token(TokenType.EOF, '', self.line, self.column))
        return tokens


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python lexer.py <archivo.txt>")
        return
    ruta = sys.argv[1]
    try:
        src = open(ruta, encoding='utf-8').read()
    except FileNotFoundError:
        print(f"Error: no existe '{ruta}'")
        return
    lexer = Lexer(src)
    tokens = lexer.tokenize()
    print("--- TOKENS ---")
    for t in tokens:
        if t.type == TokenType.EOF:
            print("EOF")
        else:
            print(f"{t.type.name:15} [ {t.value} ] -> {t.line}:{t.column}")
    if lexer.errors:
        print("\n--- LEXICAL ERRORS ---")
        for err in lexer.errors:
            print(err)


if __name__ == '__main__':
    main()
