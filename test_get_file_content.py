from typing import NamedTuple
from functions.get_file_content import get_file_content
from config import MAX_CHARS_TO_READ


class TestCase(NamedTuple):
    working_dir: str
    file_name: str


test_cases: list[TestCase] = [
    TestCase("calculator", "lorem.txt"),
    TestCase("calculator", "main.py"),
    TestCase("calculator", "pkg/calculator.py"),
    TestCase("calculator", "/bin/cat"),
    TestCase("calculator", "pkg/does_not_exist.py"),
]


def test() -> None:
    for case in test_cases:
        file_content = get_file_content(case.working_dir, case.file_name)
        content_length = len(file_content)
        is_truncated = content_length > MAX_CHARS_TO_READ
        print(f"{case.file_name} length: {content_length}")
        print(f"{case.file_name} truncated: {is_truncated}")
        if not is_truncated:
            print(file_content)
        print("")


if __name__ == "__main__":
    test()
