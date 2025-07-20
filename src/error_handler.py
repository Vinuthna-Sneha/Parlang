class ErrorHandler:
    @staticmethod
    def format_error(error, source_lines):
        if isinstance(error, SyntaxError):
            line = source_lines[error.args[0].split()[-1]]
            return f"Syntax Error: {error.args[0]}\nLine {line}:\n  {source_lines[line-1]}\nSuggestion: Check for missing semicolons or incorrect keywords."
        elif isinstance(error, SemanticError):
            return f"Semantic Error: {error.args[0]}\nSuggestion: Ensure variables are declared and types are compatible."
        return str(error)