from pathlib import Path
from pytest import fixture

from helpers import Scenario, FakeShare


@fixture
def scenario(tmp_path: Path) -> Scenario:
    result = Scenario(tmp_path)
    result.mkdirs()
    return result


@fixture
def rt1234(scenario: Scenario) -> FakeShare:
    share = scenario.new_share("rt1234")
    share.write_dummy_data()
    return share


@fixture
def rt5678(scenario: Scenario) -> FakeShare:
    share = scenario.new_share("rt5678")
    share.write_dummy_data()
    return share


@fixture
def rt1234_initial(rt1234: FakeShare) -> FakeShare:
    rt1234.write_initial_yaml("2020-01-01")
    return rt1234


@fixture
def rt1234_first_email(rt1234_initial: FakeShare) -> FakeShare:
    rt1234_initial.write_first_email_yaml("2020-01-23")
    return rt1234_initial
