from datetime import date
from pathlib import Path

from pytest import mark
from yaml import safe_load

from helpers import FakeShare, Scenario
from mftscleanup import state


def test_state_values():
    """
    Verify that we have a State Enum class (or equivalent) with the necessary.
    """
    names = [s.name for s in state.State]
    assert names == ["initial", "first_email", "second_email", "final_email", "cleanup"]
    assert state.State.initial
    assert state.State.first_email
    assert state.State.second_email
    assert state.State.final_email
    assert state.State.cleanup
    assert len(set(state.State)) == 5


@mark.xfail
def test_get_next_value_initial():
    assert state.get_next_state(state.State.initial) == state.State.first_email


@mark.xfail
def test_get_next_value_first_email():
    assert state.get_next_state(state.State.first_email) == state.State.second_email


@mark.xfail
def test_get_next_value_second_email():
    assert state.get_next_state(state.State.second_email) == state.State.final_email


@mark.xfail
def test_get_next_value_final_email():
    assert state.get_next_state(state.State.final_email) == state.State.cleanup


@mark.xfail
def test_get_next_value_cleanup():
    assert state.get_next_state(state.State.cleanup) is None


def test_metadata_fixtures(rt1234_initial: FakeShare, rt5678: FakeShare):
    """
    Make sure the fixtures do what we expect:

    Expected layout:
    |-- test_metadata_fixtures0
    |   |-- data
    |   |   |-- rt1234
    |   |   |   `-- dummy_1234_a.txt
    |   |   `-- rt5678
    |   |       `-- dummy_5678_a.txt
    |   `-- metadata_root
    |       |-- active
    |       |   `-- 1234_initial.yaml
    |       `-- archive

    Linkages:
    - fixtures link to scenario correctly
    - scenario links to directories correctly

    Contents:
    - the one YAML file is correct
    - data files are correct
    """
    scenario = rt1234_initial.scenario
    assert scenario.root.is_dir(), scenario
    assert rt5678.scenario is scenario
    assert not list(scenario.archive.glob("*"))
    meta_files = list(scenario.active.glob("*"))
    meta_file_names = [p.name for p in meta_files]
    assert meta_file_names == ["1234_initial.yaml"]
    yaml_data: dict = safe_load(meta_files[0].read_text(encoding="ascii"))
    rt1234_share_directory = yaml_data.pop("share_directory")
    assert rt1234_share_directory == str(scenario.data / "rt1234")
    assert yaml_data == {
        "email_addresses": ["fake@fake.com"],
        "number_of_files": 1,
        "registration_date": "2020-01-01",
        "rt_number": 1234,
        "total_file_size": 6,
    }
    data_paths = sorted(p for p in scenario.data.rglob("*") if p.is_file())
    assert [str(p.relative_to(scenario.data)) for p in data_paths] == [
        "rt1234/dummy_1234_a.txt",
        "rt5678/dummy_5678_a.txt",
    ]
    for p in data_paths:
        assert (scenario.data / p).read_bytes() == b"hello\n"


@mark.xfail
def test_get_active_shares_none(scenario: Scenario):
    assert list(state.get_active_shares(scenario.active)) == []


@mark.xfail
def test_get_active_shares_rt1234_initial(rt1234_initial: FakeShare):
    assert list(state.get_active_shares(rt1234_initial.scenario.active)) == ["rt1234"]


@mark.xfail
def test_get_active_shares_rt1234_initial_rt5678_pre(
    rt1234_initial: FakeShare, rt5678: FakeShare
):
    assert list(state.get_active_shares(rt1234_initial.scenario.active)) == ["rt1234"]
