class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

class Lexer:
    def __init__(self, source):
        self.source = source
        self.pos = 0
        self.line = 1

    def tokenize(self):
        tokens = []
        while self.pos < len(self.source):
            char = self.source[self.pos]
            if char.isspace():
                if char == '\n':
                    self.line += 1
                self.pos += 1
                continue
            elif char.isalpha():
                ident = self.consume_while(lambda c: c.isalnum() or c == '_')
                token_type = 'IDENT'
                if ident in ['fn', 'let', 'parfor', 'print', 'return', 'in']:
                    token_type = ident.upper()
                tokens.append(Token(token_type, ident, self.line))
            elif char.isdigit():
                number = self.consume_while(lambda c: c.isdigit())
                tokens.append(Token('NUMBER', number, self.line))
            elif char == '(':
                tokens.append(Token('LPAREN', char, self.line))
                self.pos += 1
            elif char == ')':
                tokens.append(Token('RPAREN', char, self.line))
                self.pos += 1
            elif char == '{':
                tokens.append(Token('LBRACE', char, self.line))
                self.pos += 1
            elif char == '}':
                tokens.append(Token('RBRACE', char, self.line))
                self.pos += 1
            elif char == '[':
                tokens.append(Token('LBRACKET', char, self.line))
                self.pos += 1
            elif char == ']':
                tokens.append(Token('RBRACKET', char, self.line))
                self.pos += 1
            elif char == ',':
                tokens.append(Token('COMMA', char, self.line))
                self.pos += 1
            elif char == ';':
                tokens.append(Token('SEMICOLON', char, self.line))
                self.pos += 1
            elif char == '=':
                tokens.append(Token('EQUALS', char, self.line))
                self.pos += 1
            elif char in '+-*/':
                tokens.append(Token('OPERATOR', char, self.line))
                self.pos += 1
            else:
                raise SyntaxError(f"Invalid character {char} at line {self.line}")
        return tokens

    def consume_while(self, condition):
        start = self.pos
        while self.pos < len(self.source) and condition(self.source[self.pos]):
            self.pos += 1
        return self.source[start:self.pos]