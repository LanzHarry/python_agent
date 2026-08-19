from typing import NamedTuple
from functions.write_file import write_file


class TestCase(NamedTuple):
    working_dir: str
    file_name: str
    content: str


test_cases: list[TestCase] = [
    TestCase("calculator", "lorem.txt", "wait, this isn't lorem ipsum"),
    TestCase("calculator", "pkg/morelorem.txt", "lorem impsum dolor sit amet"),
    TestCase("calculator", "/tmp/temp.txt", "this should not be allowed"),
]


def test() -> None:
    for case in test_cases:
        write_result = write_file(case.working_dir, case.file_name, case.content)
        print(write_result)
        print("")


if __name__ == "__main__":
    test()
