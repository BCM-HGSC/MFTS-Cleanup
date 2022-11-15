"""
Classes and functions to support testing.

A single share will involve one or more YAML files inside a metadata directory
along with a share-specific directory containing the shared data. A minimal
example:

    test_new_share_happy_path
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

from mftscleanup.metadata_store import MetadataStore


class Scenario:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.data = self.root / "data"
        self.metadata_store = MetadataStore(self.root / "metadata_root")
        self.metadata_root = self.metadata_store.metadata_root
        self.active = self.metadata_store.active
        self.archive = self.metadata_store.archive

    def __repr__(self):
        return f"{self.__class__.__name__}({str(self.root)!r})"

    def create(self):
        for p in (self.data, self.active, self.archive):
            p.mkdir(parents=True, exist_ok=True)
        yaml_text = dedent(
            f"""\
            from_address: sender@fake.domain
            host: SMTP.FAKE.DOMAIN
            """
        )
        yaml_file_path = self.metadata_root / "email_settings.yaml"
        yaml_file_path.write_text(yaml_text)

    def new_share(self, share_id: str) -> "FakeShare":
        return FakeShare(self, share_id)


class FakeShare:
    def __init__(self, scenario: Scenario, share_id: str):
        self.scenario = scenario
        self.metadata_store = scenario.metadata_store
        self.share_id = share_id
        self.share_root = self.scenario.data / f"{self.share_id}"
        self.share_root.mkdir()
        self.num_files = 0
        self.num_bytes = 0
        self.dummy_letters_used = set()

    def write_dummy_data(self, letter="a") -> Path:
        assert letter not in self.dummy_letters_used, f"re-used '{letter}'"
        self.dummy_letters_used.add(letter)
        payload = b"hello\n"
        dummy_file = self.share_root / f"dummy_{self.share_id}_{letter}.txt"
        dummy_file.write_bytes(payload)
        self.num_files += 1
        self.num_bytes += len(payload)
        return dummy_file

    def write_initial_yaml(self, initial_date) -> Path:
        assert list(self.share_root.glob("*")), f"empty dir {self.share_root}"
        # TODO: Define correct behavior for empty share directory. Right now, we
        # just require that all test cases contain some data.
        yaml_text = dedent(
            f"""\
            email_addresses:
            - fake@fake.com
            initial_date: '{initial_date}'
            num_bytes: {self.num_bytes}
            num_files: {self.num_files}
            share_id: {self.share_id}
            share_directory: {self.share_root}
            state: initial
            """
        )
        yaml_file_path = self.write_event_file("0000", yaml_text)
        return yaml_file_path

    def write_first_email_yaml(self, first_email_date) -> Path:
        return self.write_state_yaml("0001", first_email_date, "first_email")

    def write_state_yaml(self, event_id: str, event_date: str, state_name: str) -> Path:
        yaml_text = get_new_state_yaml(self.share_id, event_date, state_name)
        yaml_file_path = self.write_event_file(event_id, yaml_text)
        return yaml_file_path

    def write_event_file(self, event_id: str, yaml_text: str):
        yaml_file_path = self.scenario.active / f"{self.share_id}_{event_id}.yaml"
        yaml_file_path.write_text(yaml_text)
        return yaml_file_path


def get_new_state_yaml(share_id: str, event_date: str, state_name: str):
    yaml_text = dedent(
        f"""\
        {state_name}_date: '{event_date}'
        share_id: {share_id}
        """
    )
    return yaml_text
