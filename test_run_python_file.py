from functions.run_python_file import run_python_file

def test():
    print('run_python_file("calculator", "main.py")')
    result = run_python_file("calculator", "main.py")
    print(result)
    print('------ END OF TEST ------')
    print('')

    print('run_python_file("calculator", "main.py", ["3 + 5"])')
    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print(result)
    print('------ END OF TEST ------')
    print('')

    print('run_python_file("calculator", "tests.py")')
    result = run_python_file("calculator", "tests.py")
    print(result)
    print('------ END OF TEST ------')
    print('')

    print('run_python_file("calculator", "../main.py")')
    result = run_python_file("calculator", "../main.py")
    print(result)
    print('------ END OF TEST ------')
    print('')

    print('run_python_file("calculator", "nonexistent.py")')
    result = run_python_file("calculator", "nonexistent.py")
    print(result)
    print('------ END OF TEST ------')
    print('')

    print('run_python_file("calculator", "lorem.txt")')
    result = run_python_file("calculator", "lorem.txt")
    print(result)
    print('------ END OF TEST ------')

if __name__ == "__main__":
    test()