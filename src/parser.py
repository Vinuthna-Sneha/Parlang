class Node:
    def __init__(self, type, value=None, children=None):
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
        raise SyntaxError(f"Expected {expected_type} at line {self.tokens[self.pos].line if self.pos < len(self.tokens) else 'EOF'}")

    def parse(self):
        return Node("Program", children=self.parse_program())

    def parse_program(self):
        functions = []
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'FN':
            functions.append(self.parse_function())
        return functions

    def parse_function(self):
        self.consume('FN')
        ident = self.consume('IDENT')
        self.consume('LPAREN')
        self.consume('RPAREN')
        self.consume('LBRACE')
        statements = []
        while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'RBRACE':
            statements.append(self.parse_statement())
        self.consume('RBRACE')
        return Node("Function", ident.value, statements)

    def parse_statement(self):
        if self.tokens[self.pos].type == 'LET':
            return self.parse_let_stmt()
        elif self.tokens[self.pos].type == 'PARFOR':
            return self.parse_parfor_stmt()
        elif self.tokens[self.pos].type == 'PRINT':
            return self.parse_print_stmt()
        elif self.tokens[self.pos].type == 'RETURN':
            return self.parse_return_stmt()
        raise SyntaxError(f"Unexpected token {self.tokens[self.pos].type} at line {self.tokens[self.pos].line}")

    def parse_let_stmt(self):
        self.consume('LET')
        ident = self.consume('IDENT')
        self.consume('EQUALS')
        expr = self.parse_expression()
        self.consume('SEMICOLON')
        return Node("Let", ident.value, [expr])

    def parse_parfor_stmt(self):
        self.consume('PARFOR')
        ident = self.consume('IDENT')
        self.consume('IN')
        expr = self.parse_expression()
        self.consume('LBRACE')
        statements = []
        while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'RBRACE':
            statements.append(self.parse_statement())
        self.consume('RBRACE')
        return Node("ParFor", ident.value, [expr] + statements)

    def parse_print_stmt(self):
        self.consume('PRINT')
        self.consume('LPAREN')
        expr = self.parse_expression()
        self.consume('RPAREN')
        self.consume('SEMICOLON')
        return Node("Print", children=[expr])

    def parse_return_stmt(self):
        self.consume('RETURN')
        expr = self.parse_expression()
        self.consume('SEMICOLON')
        return Node("Return", children=[expr])

    def parse_expression(self):
        # Parse primary expression
        if self.tokens[self.pos].type == 'NUMBER':
            node = Node("Number", self.consume('NUMBER').value)
        elif self.tokens[self.pos].type == 'IDENT':
            node = Node("Identifier", self.consume('IDENT').value)
        elif self.tokens[self.pos].type == 'LBRACKET':
            node = self.parse_array()
        elif self.tokens[self.pos].type == 'LPAREN':
            self.consume('LPAREN')
            node = self.parse_expression()
            self.consume('RPAREN')
        else:
            raise SyntaxError(f"Unexpected token {self.tokens[self.pos].type} at line {self.tokens[self.pos].line}")

        # Handle binary operators
        while self.pos < len(self.tokens) and self.tokens[self.pos].type == 'OPERATOR':
            op = self.consume('OPERATOR')
            right = self.parse_expression()
            node = Node("BinaryExpr", op.value, [node, right])
        return node

    def parse_array(self):
        self.consume('LBRACKET')
        elements = []
        while self.pos < len(self.tokens) and self.tokens[self.pos].type != 'RBRACKET':
            elements.append(self.parse_expression())
            if self.pos < len(self.tokens) and self.tokens[self.pos].type == 'COMMA':
                self.consume('COMMA')
        self.consume('RBRACKET')
        return Node("Array", children=elements)