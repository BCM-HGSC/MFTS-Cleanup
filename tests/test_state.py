from datetime import date as D
from pathlib import Path

from pytest import mark, raises
from yaml import safe_load

from helpers import FakeShare, get_new_state_yaml, Scenario
from mftscleanup import state


def test_state_values():
    """
    Verify that we have a State Enum class (or equivalent) with the necessary.
    """
    names = [s.name for s in state.State]
    assert names == [
        "initial",
        "first_email",
        "second_email",
        "final_email",
        "cleanup",
        "hold",
    ]
    assert state.State.initial
    assert state.State.first_email
    assert state.State.second_email
    assert state.State.final_email
    assert state.State.cleanup
    assert state.State.hold
    assert len(set(state.State)) == 6


def test_state_ordering():
    S = state.State
    assert S.initial < S.first_email
    assert S.first_email < S.second_email
    assert S.second_email < S.final_email
    assert S.final_email < S.cleanup
    with raises(TypeError):  # Order comparisons to S.hold is not supported.
        S.initial < S.hold
    assert S.hold is S.hold
    assert S.hold == S.hold
    assert S.initial != S.hold
    with raises(TypeError):
        S.cleanup < 9


def test_state_next_property():
    assert state.State.initial.next == state.State.first_email
    assert state.State.first_email.next == state.State.second_email
    assert state.State.second_email.next == state.State.final_email
    assert state.State.final_email.next == state.State.cleanup
    assert state.State.cleanup.next is None
    assert state.State.hold.next is None


def test_get_next_state_initial():
    assert state.get_next_state(state.State.initial) == state.State.first_email


def test_get_next_state_first_email():
    assert state.get_next_state(state.State.first_email) == state.State.second_email


def test_get_next_state_second_email():
    assert state.get_next_state(state.State.second_email) == state.State.final_email


def test_get_next_state_final_email():
    assert state.get_next_state(state.State.final_email) == state.State.cleanup


def test_get_next_state_cleanup():
    assert state.get_next_state(state.State.cleanup) is None


def test_get_next_state_illegal_str():
    with raises(TypeError):
        state.get_next_state("initial")


def test_get_next_state_illegal_None():
    with raises(TypeError):
        state.get_next_state(None)


def test_get_next_state_illegal_false():
    with raises(TypeError):
        state.get_next_state(False)


def test_metadata_fixtures(rt1234_first_email: FakeShare, rt5678: FakeShare):
    """
    Make sure the fixtures do what we expect:

    Expected layout:
    `-- test_metadata_fixtures0
        |-- data
        |   |-- rt1234
        |   |   `-- dummy_1234_a.txt
        |   `-- rt5678
        |       `-- dummy_5678_a.txt
        `-- metadata_root
            |-- active
            |   |-- rt1234_0000.yaml
            |   `-- rt1234_0001.yaml
            `-- archive

    Linkages:
    - fixtures link to scenario correctly
    - scenario links to directories correctly

    Contents:
    - the one YAML file is correct
    - data files are correct
    """
    scenario = rt1234_first_email.scenario
    assert scenario.root.is_dir(), scenario
    assert rt5678.scenario is scenario
    assert not list(scenario.archive.glob("*"))
    meta_files = list(scenario.active.glob("*"))
    meta_file_names = sorted(p.name for p in meta_files)
    assert meta_file_names == ["rt1234_0000.yaml", "rt1234_0001.yaml"]
    yaml_data: dict = safe_load(meta_files[0].read_text(encoding="ascii"))
    rt1234_share_directory = yaml_data.pop("share_directory")
    assert rt1234_share_directory == str(scenario.data / "rt1234")
    assert yaml_data == {
        "email_addresses": ["fake@fake.com"],
        "initial_date": "2020-01-01",
        "num_bytes": 6,
        "num_files": 1,
        "share_id": "rt1234",
        "state": "initial",
    }
    data_paths = sorted(p for p in scenario.data.rglob("*") if p.is_file())
    assert [str(p.relative_to(scenario.data)) for p in data_paths] == [
        "rt1234/dummy_rt1234_a.txt",
        "rt5678/dummy_rt5678_a.txt",
    ]
    for p in data_paths:
        assert (scenario.data / p).read_bytes() == b"hello\n"


def test_get_active_shares_none(scenario: Scenario):
    assert list(state.get_active_shares(scenario.active)) == []


def test_get_active_shares_rt1234_initial(rt1234_initial: FakeShare):
    assert list(state.get_active_shares(rt1234_initial.scenario.active)) == ["rt1234"]


def test_get_active_shares_rt1234_initial_rt5678_pre(
    rt1234_initial: FakeShare, rt5678: FakeShare
):
    assert list(state.get_active_shares(rt1234_initial.scenario.active)) == ["rt1234"]


def test_get_active_shares_rt1234_first_email(rt1234_first_email: FakeShare):
    assert list(state.get_active_shares(rt1234_first_email.scenario.active)) == [
        "rt1234"
    ]


def test_get_share_state_rt1234_initial(rt1234_initial: FakeShare):
    result = state.get_share_state(rt1234_initial.scenario.active, "rt1234")
    assert result == (state.State.initial, D(2020, 1, 1))


def test_get_share_state_rt1234_first_email(rt1234_first_email: FakeShare):
    result = state.get_share_state(rt1234_first_email.scenario.active, "rt1234")
    assert result == (state.State.first_email, D(2020, 1, 23))


def test_get_share_state_rt1234_not_dict(rt1234: FakeShare):
    rt1234.write_event_file("0000", "hello there")
    with raises(state.EventNotDictError):
        state.get_share_state(rt1234.scenario.active, "rt1234")


def test_get_share_state_rt1234_corrupt(rt1234: FakeShare):
    rt1234.write_event_file("0000", "]")
    with raises(state.EventFileCorruptError):
        state.get_share_state(rt1234.scenario.active, "rt1234")


def test_get_share_state_rt1234_inconsisten(rt1234: FakeShare):
    bad_yaml = get_new_state_yaml("rt2345", "2020-01-01", "initial")
    print(bad_yaml)
    rt1234.write_event_file("0000", bad_yaml)
    with raises(state.InconsistentEventError):
        print(state.get_share_state(rt1234.scenario.active, "rt1234"))


def test_get_share_state_rt1234_bad_state(rt1234: FakeShare):
    rt1234.write_state_yaml("0000", "2020-01-01", "initiallll")
    with raises(state.BadStateError):
        print(state.get_share_state(rt1234.scenario.active, "rt1234"))


def test_get_share_state_rt1234_missing_state(rt1234: FakeShare):
    rt1234.write_event_file("0000", "share_id: rt1234")
    with raises(state.MissingStateError):
        print(state.get_share_state(rt1234.scenario.active, "rt1234"))


def test_get_share_state_rt1234_ambiguous_state(rt1234: FakeShare):
    bad_yaml = get_new_state_yaml("rt1234", "2020-01-01", "initial")
    bad_yaml += "first_email_date: '2020-01-23'\n"
    print(bad_yaml)
    rt1234.write_event_file("0000", bad_yaml)
    with raises(state.AmbiguousStateError):
        print(state.get_share_state(rt1234.scenario.active, "rt1234"))
