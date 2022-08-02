"""
Classes and functions to support testing.

A single share will involve one or more YAML files inside a metadata directory
along with a share-specific directory containing the shared data. A minimal
example:

    test_new_share_happy_path0
    +-- data
    |   +-- rt1234
    |       +-- dummy_1234.txt
    +-- metadata_root
        +-- active
        |   +-- 1234_initial.yaml
        +-- archive
"""

from pathlib import Path
from textwrap import dedent


class Scenario:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.data = self.root / "data"
        self.metadata_root = self.root / "metadata_root"
        self.active = self.metadata_root / "active"
        self.archive = self.metadata_root / "archive"

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.root)!r})"

    def mkdirs(self):
        for p in (self.data, self.active, self.archive):
            p.mkdir(parents=True, exist_ok=True)

    def new_share(self, rt_number) -> "FakeShare":
        return FakeShare(self, rt_number=rt_number)


class FakeShare:
    def __init__(self, scenario: Scenario, rt_number: int):
        self.scenario = scenario
        self.rt_number = rt_number
        self.share_root = self.scenario.data / f"rt{rt_number}"
        self.share_root.mkdir()
        self.num_files = 0
        self.num_bytes = 0
        self.dummy_letters_used = set()

    def write_dummy_data(self, letter="a") -> Path:
        assert letter not in self.dummy_letters_used, f"re-used '{letter}'"
        self.dummy_letters_used.add(letter)
        payload = b"hello\n"
        dummy_file = self.share_root / f"dummy_{self.rt_number}_{letter}.txt"
        dummy_file.write_bytes(payload)
        self.num_files += 1
        self.num_bytes += len(payload)
        return dummy_file

    def write_initial_yaml(self, initial_date) -> Path:
        assert list(self.share_root.glob("*")), f"empty dir {self.share_root}"
        # TODO: Define correct behavior for empty share directory. Right now, we
        # just require that all test cases contain some data.
        initial_yaml_file = self.scenario.active / f"{self.rt_number}_initial.yaml"
        yaml_text = dedent(
            f"""\
            email_addresses:
            - fake@fake.com
            initial_date: '{initial_date}'
            number_of_files: {self.num_files}
            rt_number: {self.rt_number}
            share_directory: {self.share_root}
            total_file_size: {self.num_bytes}
            """
        )
        initial_yaml_file.write_text(yaml_text)
        return initial_yaml_file

    def write_first_email_yaml(self, first_email_date) -> Path:
        return self.write_state_yaml("first_email", first_email_date)

    def write_state_yaml(self, state_name: str, state_date: str, ) -> Path:
        yaml_file_path = self.scenario.active / f"{self.rt_number}_{state_name}.yaml"
        yaml_text = dedent(
            f"""\
            {state_name}_date: '{state_date}'
            rt_number: {self.rt_number}
            """
        )
        yaml_file_path.write_text(yaml_text)
        return yaml_file_path
