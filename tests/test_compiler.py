import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ir_generator import IRGenerator
from src.codegen import CodeGenerator

def compile_source(source):
    lexer = Lexer(source)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    ir_gen = IRGenerator(ast)
    ir = ir_gen.generate()
    codegen = CodeGenerator(ir)
    return "\n".join(codegen.generate())

class TestCompiler(unittest.TestCase):
    def test_sample_program(self):
        source = """
        fn main() {
            let numbers = [1, 2, 3, 4, 5];
            parfor n in numbers {
                print(n * n);
            }
        }
        """
        output = compile_source(source)
        self.assertIn("PARFOR", output)
        self.assertIn("ENDPARFOR", output)
        self.assertIn("MUL", output)
        self.assertIn("PRINT", output)

if __name__ == '__main__':
    unittest.main()