from functions.get_files_info import get_files_info

def test():
    result = get_files_info("calculator", ".")
    print('get_files_info("calculator", ".")')
    print(result)
    print('')

    result = get_files_info("calculator", "pkg")
    print('get_files_info("calculator", "pkg")')
    print(result)
    print('')

    result = get_files_info("calculator", "/bin")
    print('get_files_info("calculator", "/bin")')
    print(result)
    print('')

    result = get_files_info("calculator", "../")
    print('get_files_info("calculator", "../")')
    print(result)
    print('')

if __name__ == "__main__":
    test()