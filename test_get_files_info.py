from typing import NamedTuple
from functions.get_files_info import get_files_info


class TestCase(NamedTuple):
    working_dir: str
    target_dir: str


test_cases: list[TestCase] = [
    TestCase("calculator", "."),
    TestCase("calculator", "pkg"),
    TestCase("calculator", "/bin"),
    TestCase("calculator", "../"),
]


def test() -> None:
    for case in test_cases:
        print(f"Result for target dir: {case.target_dir}")
        print(get_files_info(case.working_dir, case.target_dir))
        print("")


if __name__ == "__main__":
    test()
