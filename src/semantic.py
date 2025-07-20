class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name, type):
        if name in self.symbols:
            raise SemanticError(f"Variable {name} already declared")
        self.symbols[name] = type

    def lookup(self, name):
        if name not in self.symbols:
            raise SemanticError(f"Variable {name} not declared")
        return self.symbols[name]

class SemanticAnalyzer:
    def __init__(self, ast):
        self.ast = ast
        self.symbol_table = SymbolTable()

    def analyze(self):
        for node in self.ast.children:
            self.analyze_function(node)

    def analyze_function(self, node):
        for stmt in node.children:
            self.analyze_statement(stmt)

    def analyze_statement(self, node):
        if node.type == "Let":
            ident = node.value
            expr = node.children[0]
            expr_type = self.analyze_expression(expr)
            self.symbol_table.declare(ident, expr_type)
        elif node.type == "ParFor":
            ident = node.value
            expr = node.children[0]
            expr_type = self.analyze_expression(expr)
            if expr_type != "Array":
                raise SemanticError(f"Expected array in parfor, got {expr_type}")
            self.symbol_table.declare(ident, "Number")
            for stmt in node.children[1:]:
                self.analyze_statement(stmt)
        elif node.type == "Print":
            self.analyze_expression(node.children[0])
        elif node.type == "Return":
            self.analyze_expression(node.children[0])

    def analyze_expression(self, node):
        if node.type == "Number":
            return "Number"
        elif node.type == "Identifier":
            return self.symbol_table.lookup(node.value)
        elif node.type == "Array":
            for elem in node.children:
                if self.analyze_expression(elem) != "Number":
                    raise SemanticError("Array elements must be numbers")
            return "Array"
        elif node.type == "BinaryExpr":
            left_type = self.analyze_expression(node.children[0])
            right_type = self.analyze_expression(node.children[1])
            if left_type != "Number" or right_type != "Number":
                raise SemanticError("Binary expression requires numbers")
            return "Number"
        raise SemanticError(f"Unknown expression type: {node.type}")

class SemanticError(Exception):
    pass