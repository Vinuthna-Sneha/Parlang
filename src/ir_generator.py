class IRGenerator:
    def __init__(self, ast):
        self.ast = ast
        self.ir = []
        self.temp_count = 0

    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp

    def generate(self):
        for node in self.ast.children:
            self.generate_function(node)
        return self.ir

    def generate_function(self, node):
        self.ir.append(f"func {node.value}")
        for stmt in node.children:
            self.generate_statement(stmt)
        self.ir.append("endfunc")

    def generate_statement(self, node):
        if node.type == "Let":
            ident = node.value
            expr_result = self.generate_expression(node.children[0])
            self.ir.append(f"store {expr_result}, {ident}")
        elif node.type == "ParFor":
            ident = node.value
            array = self.generate_expression(node.children[0])
            loop_label = self.new_temp()
            self.ir.append(f"parfor {ident} in {array} {loop_label}")
            for stmt in node.children[1:]:
                self.generate_statement(stmt)
            self.ir.append(f"endparfor {loop_label}")
        elif node.type == "Print":
            expr_result = self.generate_expression(node.children[0])
            self.ir.append(f"print {expr_result}")
        elif node.type == "Return":
            expr_result = self.generate_expression(node.children[0])
            self.ir.append(f"return {expr_result}")

    def generate_expression(self, node):
        if node.type == "Number":
            temp = self.new_temp()
            self.ir.append(f"const {node.value}, {temp}")
            return temp
        elif node.type == "Identifier":
            return node.value
        elif node.type == "Array":
            temp = self.new_temp()
            elements = [self.generate_expression(elem) for elem in node.children]
            self.ir.append(f"array {','.join(elements)}, {temp}, {len(elements)}")
            return temp
        elif node.type == "BinaryExpr":
            left = self.generate_expression(node.children[0])
            right = self.generate_expression(node.children[1])
            temp = self.new_temp()
            self.ir.append(f"op {node.value}, {left}, {right}, {temp}")
            return temp