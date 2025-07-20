import re

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
        self.tokens = []
        self.token_spec = [
            ('NUMBER',   r'\d+'),           # Integer
            ('IDENT',    r'[a-zA-Z]\w*'),  # Identifiers
            ('LBRACE',   r'\{'),           # {
            ('RBRACE',   r'\}'),           # }
            ('LPAREN',   r'\('),           # (
            ('RPAREN',   r'\)'),           # )
            ('LBRACKET', r'\['),           # [
            ('RBRACKET', r'\]'),           # ]
            ('SEMICOLON', r';'),           # ;
            ('COMMA',    r','),            # ,
            ('OPERATOR', r'\+|-|\*|\/'),   # Operators
            ('EQUALS',   r'='),            # = (Added)
            ('WHITESPACE', r'\s+'),        # Whitespace
        ]
        self.token_re = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in self.token_spec)
        self.keywords = {'fn', 'let', 'parfor', 'in', 'print', 'return'}

    def tokenize(self):
        for match in re.finditer(self.token_re, self.source):
            type = match.lastgroup
            value = match.group()
            if type == 'WHITESPACE':
                if '\n' in value:
                    self.line += value.count('\n')
                continue
            if type == 'IDENT' and value in self.keywords:
                type = value.upper()
            self.tokens.append(Token(type, value, self.line))
        return self.tokens