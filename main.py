import sys
from src.lexer import Lexer
from src.parser import Parser
from src.semantic import SemanticAnalyzer, SemanticError
from src.ir_generator import IRGenerator
from src.optimizer import Optimizer
from src.codegen import CodeGenerator
from src.error_handler import ErrorHandler

def compile_file(filepath):
    try:
        with open(filepath, 'r') as file:
            source = file.read()
        
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
    except FileNotFoundError:
        return f"Error: File {filepath} not found"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_file>")
        sys.exit(1)
    result = compile_file(sys.argv[1])
    print(result)