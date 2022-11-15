from datetime import date as D

from pytest import mark, raises

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


"""
      January               February               March          
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  
          1  2  3  4                     1   1  2  3  4  5  6  7  
 5  6  7  8  9 10 11   2  3  4  5  6  7  8   8  9 10 11 12 13 14  
12 13 14 15 16 17 18   9 10 11 12 13 14 15  15 16 17 18 19 20 21  
19 20 21 22 23 24 25  16 17 18 19 20 21 22  22 23 24 25 26 27 28  
26 27 28 29 30 31     23 24 25 26 27 28 29  29 30 31              
                                                                  

       April                  May                   June          
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  
          1  2  3  4                  1  2      1  2  3  4  5  6  
 5  6  7  8  9 10 11   3  4  5  6  7  8  9   7  8  9 10 11 12 13  
12 13 14 15 16 17 18  10 11 12 13 14 15 16  14 15 16 17 18 19 20  
19 20 21 22 23 24 25  17 18 19 20 21 22 23  21 22 23 24 25 26 27  
26 27 28 29 30        24 25 26 27 28 29 30  28 29 30              
                      31                                          

        July                 August              September        
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  
          1  2  3  4                     1         1  2  3  4  5  
 5  6  7  8  9 10 11   2  3  4  5  6  7  8   6  7  8  9 10 11 12  
12 13 14 15 16 17 18   9 10 11 12 13 14 15  13 14 15 16 17 18 19  
19 20 21 22 23 24 25  16 17 18 19 20 21 22  20 21 22 23 24 25 26  
26 27 28 29 30 31     23 24 25 26 27 28 29  27 28 29 30           
                      30 31                                       

      October               November              December        
Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  Su Mo Tu We Th Fr Sa  
             1  2  3   1  2  3  4  5  6  7         1  2  3  4  5  
 4  5  6  7  8  9 10   8  9 10 11 12 13 14   6  7  8  9 10 11 12  
11 12 13 14 15 16 17  15 16 17 18 19 20 21  13 14 15 16 17 18 19  
18 19 20 21 22 23 24  22 23 24 25 26 27 28  20 21 22 23 24 25 26  
25 26 27 28 29 30 31  29 30                 27 28 29 30 31   
"""


@mark.parametrize(
    "test_case",
    [
        # Note that MLK day on the 20 shifts all subsequent dates.
        "initial       2020-01-01  first_email  2020-01-23",
        "first_email   2020-01-23  second_email 2020-01-28",
        "second_email  2020-01-28  final_email  2020-01-29",
        "final_email   2020-01-29  cleanup      2020-01-30",
        "cleanup       2020-01-30  None         None",
        # Test cases for a share that missed all holidays:
        "initial       2020-08-03  first_email  2020-08-24",
        "first_email   2020-08-24  second_email 2020-08-27",
        "second_email  2020-08-27  final_email  2020-08-28",
        "final_email   2020-08-28  cleanup      2020-08-31",
        "cleanup       2020-08-31  None         None",
        # Test cases for a share that spans the Thanksgiving weekend:
        "initial       2020-11-05  first_email  2020-11-30",
        #    Thanksgiving and Black Friday fall on the 26th and 27th
        "first_email   2020-11-30  second_email 2020-12-03",
        "second_email  2020-12-03  final_email  2020-12-04",
        "final_email   2020-12-04  cleanup      2020-12-07",
        "cleanup       2020-12-07  None         None",
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
