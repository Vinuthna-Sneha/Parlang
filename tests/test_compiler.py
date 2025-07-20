from lexer import Lexer
from parser import Parser
from semantic import SemanticAnalyzer
from ir_generator import IRGenerator
from optimizer import Optimizer
from codegen import CodeGenerator
from error_handler import ErrorHandler

def compile(source):
    try:
        # Tokenize
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        # Parse
        parser = Parser(tokens)
        ast = parser.parse()

        # Semantic Analysis
        analyzer = SemanticAnalyzer(ast)
        analyzer.analyze()

        # Generate IR
        ir_gen = IRGenerator(ast)
        ir = ir_gen.generate()

        # Optimize
        optimizer = Optimizer(ir)
        optimized_ir = optimizer.optimize()

        # Generate Code
        codegen = CodeGenerator(optimized_ir)
        code = codegen.generate()

        return "\n".join(code)
    except (SyntaxError, SemanticError) as e:
        source_lines = {i+1: line for i, line in enumerate(source.split('\n'))}
        return ErrorHandler.format_error(e, source_lines)

# Test
source = """
fn main() {
    let numbers = [1, 2, 3, 4, 5];
    parfor n in numbers {
        print(n * n);
    }
}
"""
print(compile(source))