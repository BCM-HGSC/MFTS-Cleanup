from datetime import date as D

from pytest import raises
from yaml import safe_load

from helpers import FakeShare, get_new_state_yaml, Scenario
from mftscleanup import metadata_store, state


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
        "sponsor_id": "fake_sponsor",
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
    assert list(scenario.metadata_store.get_active_shares()) == []


def test_get_active_shares_rt1234_initial(rt1234_initial: FakeShare):
    assert list(rt1234_initial.metadata_store.get_active_shares()) == ["rt1234"]


def test_get_active_shares_rt1234_initial_rt5678_pre(
    rt1234_initial: FakeShare, rt5678: FakeShare
):
    assert list(rt1234_initial.metadata_store.get_active_shares()) == ["rt1234"]


def test_get_active_shares_rt1234_first_email(rt1234_first_email: FakeShare):
    assert list(rt1234_first_email.metadata_store.get_active_shares()) == ["rt1234"]


def test_get_share_state_rt1234_initial(rt1234_initial: FakeShare):
    result = rt1234_initial.metadata_store.get_share_state("rt1234")
    assert result == (state.State.INITIAL, D(2020, 1, 1))


def test_get_share_state_rt1234_first_email(rt1234_first_email: FakeShare):
    result = rt1234_first_email.metadata_store.get_share_state("rt1234")
    assert result == (state.State.FIRST_EMAIL, D(2020, 1, 23))


def test_get_share_state_rt1234_not_dict(rt1234: FakeShare):
    rt1234.write_event_file("0000", "hello there")
    with raises(metadata_store.EventNotDictError):
        rt1234.metadata_store.get_share_state("rt1234")


def test_get_share_state_rt1234_corrupt(rt1234: FakeShare):
    rt1234.write_event_file("0000", "]")
    with raises(metadata_store.EventFileCorruptError):
        rt1234.metadata_store.get_share_state("rt1234")


def test_get_share_state_rt1234_inconsisten(rt1234: FakeShare):
    bad_yaml = get_new_state_yaml("rt2345", "2020-01-01", "initial")
    print(bad_yaml)
    rt1234.write_event_file("0000", bad_yaml)
    with raises(metadata_store.InconsistentEventError):
        print(rt1234.metadata_store.get_share_state("rt1234"))


def test_get_share_state_rt1234_bad_state(rt1234: FakeShare):
    rt1234.write_state_yaml("0000", "2020-01-01", "initiallll")
    with raises(metadata_store.BadStateError):
        print(rt1234.metadata_store.get_share_state("rt1234"))


def test_get_share_state_rt1234_missing_state(rt1234: FakeShare):
    rt1234.write_event_file("0000", "share_id: rt1234")
    with raises(metadata_store.MissingStateError):
        print(rt1234.metadata_store.get_share_state("rt1234"))


def test_get_share_state_rt1234_ambiguous_state(rt1234: FakeShare):
    bad_yaml = get_new_state_yaml("rt1234", "2020-01-01", "initial")
    bad_yaml += "first_email_date: '2020-01-23'\n"
    print(bad_yaml)
    rt1234.write_event_file("0000", bad_yaml)
    with raises(metadata_store.AmbiguousStateError):
        print(rt1234.metadata_store.get_share_state("rt1234"))
