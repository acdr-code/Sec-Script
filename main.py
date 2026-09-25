import sys
import interpreter

#warning stop
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python main.py <file.sec>", file=sys.stderr)
        sys.exit(1)

    interpreter.run_file(sys.argv[1])