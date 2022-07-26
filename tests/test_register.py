from datetime import date
from pathlib import Path
from textwrap import dedent

from mftscleanup import cleanup


def test_new_share_happy_path(tmp_path: Path):
    # Phase 1: setup.
    root = tmp_path
    active = root / "active"
    share = root / "rt1234"
    active.mkdir()
    share.mkdir()
    dummy_file = share / "dummy.txt"
    dummy_file.write_bytes(b"hello\n")
    print(repr(active))
    # Phase 2: run the code you are testing.
    cleanup.new_share(
        root,
        "1234",
        share,
        ["fake@fake.com"],
        date(2020, 1, 1),
    )
    # Phase 3: check the results.
    yaml_path = active / "1234_initial.yaml"
    assert yaml_path.is_file()
    EXPECTED_YAML = dedent(
        f"""\
        email_addresses:
        - fake@fake.com
        number_of_files: 1
        registration_date: '2020-01-01'
        rt_number: 1234
        share_directory: {share}
        total_file_size: 6
        """
    )
    assert yaml_path.read_text() == EXPECTED_YAML
