class Node:
    def __init__(self, type, value, children=None):
        self.type = type
        self.value = value
        self.children = children or []

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def consume(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos].type == expected_type:
            token = self.tokens[self.pos]
            self.pos += 1
            return token
        expected_line = self.tokens[self.pos].line if self.pos < len(self.tokens) else 'EOF'
        actual_token = self.tokens[self.pos].type if self.pos < len(self.tokens) else 'EOF'
        raise SyntaxError(f"Expected {expected_type} but found {actual_token} at line {expected_line}")

    def parse(self):
        nodes = []
        while self.pos < len(self.tokens):
            if self.tokens[self.pos].type == 'FN':
                nodes.append(self.parse_function())
            else:
                raise SyntaxError(f"Unexpected token {self.tokens[self.pos].type} at line {self.tokens[self.pos].line}")
        return Node("Program", None, nodes)

    def parse_function(self):
        self.consume('FN')
        ident = self.consume('IDENT').value
        self.consume('LPAREN')
        self.consume('RPAREN')
        self.consume('LBRACE')
        statements = []
        while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'RBRACE':
            statements.append(self.parse_statement())
        self.consume('RBRACE')
        return Node("Function", ident, statements)

    def parse_statement(self):
        if self.tokens[self.pos].type == 'LET':
            return self.parse_let()
        elif self.tokens[self.pos].type == 'PARFOR':
            return self.parse_parfor()
        elif self.tokens[self.pos].type == 'PRINT':
            return self.parse_print()
        elif self.tokens[self.pos].type == 'RETURN':
            return self.parse_return()
        else:
            raise SyntaxError(f"Unexpected token {self.tokens[self.pos].type} at line {self.tokens[self.pos].line}")

    def parse_let(self):
        self.consume('LET')
        ident = self.consume('IDENT').value
        self.consume('EQUALS')
        expr = self.parse_expression()
        self.consume('SEMICOLON')
        return Node("Let", ident, [expr])

    def parse_parfor(self):
        self.consume('PARFOR')
        ident = self.consume('IDENT').value
        self.consume('IN')
        array = self.parse_expression()
        self.consume('LBRACE')
        statements = []
        while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'RBRACE':
            statements.append(self.parse_statement())
        self.consume('RBRACE')
        return Node("ParFor", ident, [array] + statements)

    def parse_print(self):
        self.consume('PRINT')
        self.consume('LPAREN')
        expr = self.parse_expression()
        self.consume('RPAREN')
        self.consume('SEMICOLON')
        return Node("Print", None, [expr])

    def parse_return(self):
        self.consume('RETURN')
        expr = self.parse_expression()
        self.consume('SEMICOLON')
        return Node("Return", None, [expr])

    def parse_expression(self, min_precedence=0):
        node = self.parse_primary()
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'OPERATOR':
            op = self.tokens[self.pos].value
            precedence = {'+': 1, '-': 1, '*': 2, '/': 2}.get(op, 0)
            if precedence < min_precedence:
                break
            self.consume('OPERATOR')
            right = self.parse_expression(precedence + 1)
            node = Node("BinaryExpr", op, [node, right])
        return node

    def parse_primary(self):
        if self.tokens[self.pos].type == 'NUMBER':
            return Node("Number", self.consume('NUMBER').value)
        elif self.tokens[self.pos].type == 'IDENT':
            return Node("Identifier", self.consume('IDENT').value)
        elif self.tokens[self.pos].type == 'LBRACKET':
            return self.parse_array()
        elif self.tokens[self.pos].type == 'LPAREN':
            self.consume('LPAREN')
            expr = self.parse_expression()
            self.consume('RPAREN')
            return expr
        else:
            raise SyntaxError(f"Unexpected token {self.tokens[self.pos].type} at line {self.tokens[self.pos].line}")

    def parse_array(self):
        self.consume('LBRACKET')
        elements = []
        if self.pos < len(self.tokens) and self.tokens[self.pos].type != 'RBRACKET':
            elements.append(self.parse_expression())
            while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'COMMA':
                self.consume('COMMA')
                elements.append(self.parse_expression())
        self.consume('RBRACKET')
        return Node("Array", None, elements)