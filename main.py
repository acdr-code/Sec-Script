import sys
from Grammar import parser
from AST import ASTBuilder
import interpreter


def run_file(filepath: str):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            code = f.read()
    except FileNotFoundError:
        print(f"ERROR// NO FILE FOUND WITH NAME {filepath}", file=sys.stderr)
        sys.exit(1)

    tree = parser.parse(code)
    ast_statements = ASTBuilder().transform(tree)

    for stmt in ast_statements:
        interpreter.interpret(stmt)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python main.py <file.sec>", file=sys.stderr)
        sys.exit(1)

    run_file(sys.argv[1])