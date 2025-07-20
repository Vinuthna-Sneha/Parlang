class ErrorHandler:
    @staticmethod
    def format_error(error, source_lines):
        if isinstance(error, SyntaxError):
            # Extract line number from error message
            import re
            match = re.search(r'line (\d+)', str(error))
            line_num = int(match.group(1)) if match else 1
            line_text = source_lines.get(line_num, "<unknown>")
            return f"Syntax Error: {str(error)}\nLine {line_num}:\n  {line_text}\nSuggestion: Check for missing semicolons or incorrect keywords."
        elif isinstance(error, SemanticError):
            return f"Semantic Error: {str(error)}\nSuggestion: Ensure variables are declared and types are compatible."
        return str(error)