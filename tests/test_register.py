from datetime import date
from pathlib import Path
from textwrap import dedent

from mftscleanup import cleanup
from helpers import FakeShare


def test_new_share_happy_path(rt1234: FakeShare):
    # Phase 1: setup.
    pass  # Alreadly handled in rt1234.
    # Phase 2: run the code you are testing.
    cleanup.new_share(
        rt1234.scenario.metadata_root,
        "rt1234",
        rt1234.share_root,
        ["fake@fake.com"],
        date(2020, 1, 1),
    )
    # Phase 3: check the results.
    yaml_path = rt1234.scenario.active / "rt1234_0000.yaml"
    assert yaml_path.is_file()
    EXPECTED_YAML = dedent(
        f"""\
        email_addresses:
        - fake@fake.com
        initial_date: '2020-01-01'
        num_bytes: {rt1234.num_bytes}
        num_files: {rt1234.num_files}
        share_directory: {rt1234.share_root}
        share_id: {rt1234.share_id}
        state: initial
        """
    )
    assert yaml_path.read_text() == EXPECTED_YAML
