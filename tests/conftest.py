from pathlib import Path
from turtle import rt

from pytest import fixture

from helpers import Scenario, FakeShare


@fixture
def scenario(tmp_path: Path) -> Scenario:
    result = Scenario(tmp_path)
    result.mkdirs()
    return result


@fixture
def rt1234(scenario: Scenario) -> FakeShare:
    share = scenario.new_share(1234)
    share.write_dummy_data()
    return share


@fixture
def rt5678(scenario: Scenario) -> FakeShare:
    share = scenario.new_share(5678)
    share.write_dummy_data()
    return share


@fixture
def rt1234_initial(rt1234: FakeShare) -> FakeShare:
    rt1234.write_initial_yaml("2020-01-01")
    # initial_yaml(rt1234, 1234, "2020-01-01")
    return rt1234
