import sys
import argparse
from pkg.calculator import Calculator
from pkg.render import format_json_output


def main():
    parser = argparse.ArgumentParser(description="Calculator App")
    parser.add_argument("expression", nargs="*", help="The expression to evaluate")
    parser.add_argument("--file", "-f", help="Path to a file containing the expression")
    args = parser.parse_args()

    calculator = Calculator()
    expression = ""

    if args.file:
        try:
            with open(args.file, "r") as f:
                expression = f.read().strip()
        except FileNotFoundError:
            print(f"Error: File not found at {args.file}")
            return
    elif args.expression:
        expression = " ".join(args.expression)
    else:
        print("Calculator App")
        print('Usage: python main.py "<expression>"')
        print('Example: python main.py "( 3 + 5 ) * 2"')
        print('Or: python main.py --file <filename>')
        print('Example: python main.py --file expression.txt')
        return

    try:
        result = calculator.evaluate(expression)
        if result is not None:
            to_print = format_json_output(expression, result)
            print(to_print)
        else:
            print("Error: Expression is empty or contains only whitespace.")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()