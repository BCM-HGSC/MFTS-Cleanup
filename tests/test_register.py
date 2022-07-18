from datetime import date
from pathlib import Path
from shutil import rmtree

from mftscleanup import cleanup


def test_a():
    # Phase 1: setup.
    root = Path("build/test/cleanup-root")
    rmtree(root)
    # Phase 2: run the code you are testing.
    cleanup.new_share(
        root,
        "1234",
        "build/test/rt1234",
        ["fake@fake.com"],
        3,
        99,
        date(2020, 1, 1),
    )
    # Phase 3: check the results.
    yaml_path = Path(root) / "active" / "1234_initial.yaml"
    assert yaml_path.is_file()
    EXPECTED_YAML = """\
email_addresses:
- fake@fake.com
number_of_files: 3
registration_date: '2020-01-01'
rt_number: 1234
share_directory: build/test/rt1234
total_file_size: 99
"""
    assert yaml_path.read_text() == EXPECTED_YAML
