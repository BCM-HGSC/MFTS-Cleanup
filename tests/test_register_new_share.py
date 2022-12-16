from datetime import date
from shutil import which
from sys import executable
from subprocess import run
from textwrap import dedent

from mftscleanup import __main__
from mftscleanup import cleanup
from mftscleanup import metadata_store
from helpers import FakeShare


def test_new_share_happy_path(rt1234: FakeShare):
    """
    Invoke the cleanup.new_share function from within the pytest process.
    """
    # Phase 1: setup.
    pass  # Alreadly handled in rt1234.
    # Phase 2: run the code you are testing.
    cleanup.new_share(
        metadata_store.MetadataStore(rt1234.scenario.metadata_root),
        "dummy_sponsor_id",
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
        sponsor_id: dummy_sponsor_id
        state: initial
        """
    )
    assert yaml_path.read_text() == EXPECTED_YAML


def test_new_share_via_main(rt1234: FakeShare):
    """
    Invoke the top-level main function from within the pytest process.
    """
    today_str = date.today().isoformat()
    argv = [
        "new",
        str(rt1234.scenario.metadata_root),
        "dummy_sponsor_id",
        "1234",
        str(rt1234.share_root),
        "fake@fake.com",
    ]
    __main__.main(argv)
    yaml_path = rt1234.scenario.active / "rt1234_0000.yaml"
    assert yaml_path.is_file()
    EXPECTED_YAML = dedent(
        f"""\
        email_addresses:
        - fake@fake.com
        initial_date: '{today_str}'
        num_bytes: {rt1234.num_bytes}
        num_files: {rt1234.num_files}
        share_directory: {rt1234.share_root}
        share_id: {rt1234.share_id}
        sponsor_id: dummy_sponsor_id
        state: initial
        """
    )
    assert yaml_path.read_text() == EXPECTED_YAML


def test_new_share_python_command(rt1234: FakeShare):
    """
    Invoke the top-level main function in a new Python process by using:
    `python -m mftscleanup new ...`
    """
    today_str = date.today().isoformat()
    print(executable)
    assert executable
    command = [
        executable,
        "-m",
        "mftscleanup",
        "new",
        str(rt1234.scenario.metadata_root),
        "dummy_sponsor_id",
        "1234",
        str(rt1234.share_root),
        "fake@fake.com",
    ]
    completed_process = run(command)
    assert completed_process.returncode == 0
    yaml_path = rt1234.scenario.active / "rt1234_0000.yaml"
    assert yaml_path.is_file()
    EXPECTED_YAML = dedent(
        f"""\
        email_addresses:
        - fake@fake.com
        initial_date: '{today_str}'
        num_bytes: {rt1234.num_bytes}
        num_files: {rt1234.num_files}
        share_directory: {rt1234.share_root}
        share_id: {rt1234.share_id}
        sponsor_id: dummy_sponsor_id
        state: initial
        """
    )
    assert yaml_path.read_text() == EXPECTED_YAML


def test_new_share_shell_command(rt1234: FakeShare):
    """
    Invoke the register_new_share function in a new Python process by using:
    `/path/to/register-new-share ...`
    """
    today_str = date.today().isoformat()
    executable_script_path = which("register-new-share")
    print(executable_script_path)
    assert executable_script_path
    command = [
        executable_script_path,
        str(rt1234.scenario.metadata_root),
        "dummy_sponsor_id",
        "1234",
        str(rt1234.share_root),
        "fake@fake.com",
    ]
    completed_process = run(command)
    assert completed_process.returncode == 0
    yaml_path = rt1234.scenario.active / "rt1234_0000.yaml"
    assert yaml_path.is_file()
    EXPECTED_YAML = dedent(
        f"""\
        email_addresses:
        - fake@fake.com
        initial_date: '{today_str}'
        num_bytes: {rt1234.num_bytes}
        num_files: {rt1234.num_files}
        share_directory: {rt1234.share_root}
        share_id: {rt1234.share_id}
        sponsor_id: dummy_sponsor_id
        state: initial
        """
    )
    assert yaml_path.read_text() == EXPECTED_YAML
