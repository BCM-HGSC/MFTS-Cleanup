from datetime import date as D

from pytest import mark, raises

from mftscleanup import state


def test_state_values():
    """
    Verify that we have a State Enum class (or equivalent) with the necessary.
    """
    names = [s.name for s in state.State]
    assert names == [
        "INITIAL",
        "FIRST_EMAIL",
        "SECOND_EMAIL",
        "FINAL_EMAIL",
        "CLEANUP",
        "HOLD",
    ]
    assert state.State.INITIAL
    assert state.State.FIRST_EMAIL
    assert state.State.SECOND_EMAIL
    assert state.State.FINAL_EMAIL
    assert state.State.CLEANUP
    assert state.State.HOLD
    assert len(set(state.State)) == 6


def test_state_ordering():
    S = state.State
    assert S.INITIAL < S.FIRST_EMAIL
    assert S.FIRST_EMAIL < S.SECOND_EMAIL
    assert S.SECOND_EMAIL < S.FINAL_EMAIL
    assert S.FINAL_EMAIL < S.CLEANUP
    with raises(TypeError):  # Order comparisons to S.HOLD is not supported.
        _ = S.INITIAL < S.HOLD
    assert S.HOLD is S.HOLD
    assert S.HOLD == S.HOLD
    assert S.INITIAL != S.HOLD
    with raises(TypeError):
        _ = S.CLEANUP < 9


def test_state_next_property():
    assert state.State.INITIAL.next is state.State.FIRST_EMAIL
    assert state.State.FIRST_EMAIL.next is state.State.SECOND_EMAIL
    assert state.State.SECOND_EMAIL.next is state.State.FINAL_EMAIL
    assert state.State.FINAL_EMAIL.next is state.State.CLEANUP
    assert state.State.CLEANUP.next is state.State.CLEANUP
    assert state.State.HOLD.next is state.State.HOLD


"""
    January 2020
Su Mo Tu We Th Fr Sa
          H  H  3  4  <- Winter Break
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 ML 21 22 23 24 25  <- MLK Day
26 27 28 29 30 31
"""


@mark.parametrize(
    "test_case",
    [
        # Note that MLK day on the 20 shifts all subsequent dates.
        "INITIAL       2020-01-01  FIRST_EMAIL  2020-01-24",
        "FIRST_EMAIL   2020-01-24  SECOND_EMAIL 2020-01-29",
        "SECOND_EMAIL  2020-01-29  FINAL_EMAIL  2020-01-30",
        "FINAL_EMAIL   2020-01-30  CLEANUP      2020-01-31",
        "CLEANUP       2020-01-31  CLEANUP         None",
        # Test cases for a share that missed all holidays:
        "INITIAL       2020-08-03  FIRST_EMAIL  2020-08-24",
        "FIRST_EMAIL   2020-08-24  SECOND_EMAIL 2020-08-27",
        "SECOND_EMAIL  2020-08-27  FINAL_EMAIL  2020-08-28",
        "FINAL_EMAIL   2020-08-28  CLEANUP      2020-08-31",
        "CLEANUP       2020-08-31  CLEANUP         None",
        # Test cases for a share that spans the Thanksgiving weekend:
        # November 2020
        # Su Mo Tu We Th Fr Sa
        #  1  2  3  4  5  6  7
        #  8  9 10 11 12 13 14
        # 15 16 17 18 19 20 21
        # 22 23 24 25 TG BF 28  <- Thanksgiving, Black Friday
        # 29 30
        #
        # December 2020
        # Su Mo Tu We Th Fr Sa
        #        1  2  3  4  5
        #  6  7  8  9 10 11 12
        "INITIAL       2020-11-05  FIRST_EMAIL  2020-11-30",
        #    Thanksgiving and Black Friday fall on the 26th and 27th
        "FIRST_EMAIL   2020-11-30  SECOND_EMAIL 2020-12-03",
        "SECOND_EMAIL  2020-12-03  FINAL_EMAIL  2020-12-04",
        "FINAL_EMAIL   2020-12-04  CLEANUP      2020-12-07",
        "CLEANUP       2020-12-07  CLEANUP         None",
        "HOLD          2020-12-07  HOLD            None",
    ],
)
def test_get_transition(test_case: str):
    start_state_str, start_date_str, new_state_str, new_date_str = test_case.split()
    start_state = state.State[start_state_str]
    start_date = D.fromisoformat(start_date_str)
    expect_new_state = None if new_state_str == "None" else state.State[new_state_str]
    expect_new_date = None if new_date_str == "None" else D.fromisoformat(new_date_str)
    print(start_state, start_date, expect_new_state, expect_new_date)
    new_state, new_date = state.get_transition(start_state, start_date)
    assert new_state == expect_new_state
    assert new_date == expect_new_date


def test_get_state_illegal_str():
    with raises(KeyError):
        state.State["initial"]


def test_get_state_illegal_None():
    with raises(KeyError):
        state.State[None]  # type: ignore


def test_get_state_illegal_false():
    with raises(KeyError):
        state.State[False]  # type: ignore
