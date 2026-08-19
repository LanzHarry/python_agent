from typing import NamedTuple
from functions.run_python_file import run_python_file


class TestCase(NamedTuple):
    working_dir: str
    file_name: str
    args: list[str] | None = None


test_cases: list[TestCase] = [
    TestCase("calculator", "main.py"),
    TestCase("calculator", "main.py", ["3 + 5"]),
    TestCase("calculator", "tests.py"),
    TestCase("calculator", "../main.py"),
    TestCase("calculator", "nonexistent.py"),
    TestCase("calculator", "lorem.txt"),
]


def test() -> None:
    for case in test_cases:
        run_result = run_python_file(case.working_dir, case.file_name, case.args)
        print(run_result)
        print("")


if __name__ == "__main__":
    test()
