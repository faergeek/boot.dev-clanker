from functions.get_files_info import get_files_info


def test_the_thing(output: str):
    print("\n".join(f"  {line}" for line in output.split("\n")))


def main():
    print("Result for current directory:")
    test_the_thing(get_files_info("calculator", "."))

    print("Result for 'pkg' directory:")
    test_the_thing(get_files_info("calculator", "pkg"))

    print("Result for '/bin' directory:")
    test_the_thing(get_files_info("calculator", "/bin"))

    print("Result for '../' directory:")
    test_the_thing(get_files_info("calculator", "../"))


if __name__ == "__main__":
    main()
