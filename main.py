import sys
import interpreter
from lark.exceptions import UnexpectedCharacters, UnexpectedEOF, UnexpectedToken, VisitError

#warning stop
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python main.py <file.sec>", file=sys.stderr)
        sys.exit(1)

    try:
        interpreter.run_file(sys.argv[1])
    
    #low level error handeling:
    except interpreter.SecScriptError as e: #for debug mode, in publish mode, this will change to all specific errors
        print(e, file=sys.stderr)
        sys.exit(1)

    except UnexpectedCharacters as e:
        print(f"[line {e.line}] Unexpected characters '{e.char}'", file=sys.stderr)
        sys.exit(1)

    except UnexpectedToken as e:
        print(f"[line {e.line}] Unexpected token '{e.token}'", file=sys.stderr)
        sys.exit(1)

    except UnexpectedEOF as e:
        print(f"[line {e.line}] UnexpectedEOF: syntax error, unexpected end of file", file=sys.stderr)
        sys.exit(1)

    except VisitError as e:
        print(f"AST ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)