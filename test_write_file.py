from functions.write_file import write_file

def test():
    result = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print('write_file("calculator", "lorem.txt", "wait, this isn\'t lorem ipsum")')
    print(result)
    print('------ END OF TEST ------')
    print('------ END OF TEST ------')
    print('')

    result = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print('write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")')
    print(result)
    print('------ END OF TEST ------')
    print('')

    result = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print('write_file("calculator", "/tmp/temp.txt", "this should not be allowed")')
    print(result)
    print('------ END OF TEST ------')
    print('')

if __name__ == "__main__":
    test()