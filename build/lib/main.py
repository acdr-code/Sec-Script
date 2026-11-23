import sys
import argparse
import warnings

from core import interpreter
from lark.exceptions import (
    UnexpectedCharacters,
    UnexpectedEOF,
    UnexpectedToken,
    VisitError
)

warnings.filterwarnings("ignore", category=DeprecationWarning)


def main():
    parser = argparse.ArgumentParser(
        prog="seclang",
        description="SecScript Language Interpreter"
    )

    parser.add_argument("file", help="Path to SecScript source file")

    args = parser.parse_args()

    try:
        interpreter.run_file(args.file)

    except interpreter.SecScriptError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    except UnexpectedCharacters as e:
        print(f"[line {e.line}] Unexpected characters '{e.char}'", file=sys.stderr)
        sys.exit(1)

    except UnexpectedToken as e:
        print(f"[line {e.line}] Unexpected token '{e.token}'", file=sys.stderr)
        sys.exit(1)

    except UnexpectedEOF as e:
        print(
            f"[line {e.line}] UnexpectedEOF: syntax error, unexpected end of file",
            file=sys.stderr
        )
        sys.exit(1)

    except VisitError as e:
        print(f"AST ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()