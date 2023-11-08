from datetime import date as D

from pytest import mark

from mftscleanup.state import get_deletion_date, State


"""
        January 2023
Su Mo Tu We Th Fr Sa
 1  2  3  4  5  6  7
 8  9 10 11 12 13 14
15 MLK 17 18 19 20 21
22 23 24 25 26 27 28
29 30 31

   February 2023
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28
"""


def test_mlk():
    assert get_deletion_date(State.INITIAL, D(2023, 1, 9)) == D(2023, 2, 7)
    assert get_deletion_date(State.FIRST_EMAIL, D(2023, 1, 13)) == D(2023, 1, 23)


# @mark.xfail
def test_no_holiday():
    """
    March 2023
    Su Mo Tu We Th Fr Sa
              1  2  3  4
     5  6  7  8  9 10 11
    12 13 14 15 16 SP 18 --> St Patrick's day
    19 20 21 22  S 24 25  --> S = Start Date
    26 27 28 29 30 31

         April 2023
    Su Mo Tu We Th Fr Sa
                       1
     2  3  4  5  6  7  8
     9 10 11 12 13 14 15
    16 17 18 19 20 21 22
    23 24 25 26 27 28 29
    30
    """
    start = D(2023, 3, 23)
    assert get_deletion_date(State.INITIAL, start) == D(2023, 4, 21)
    #     assert get_deletion_date(State.FIRST_EMAIL, start) == D(2023, 3, 31)
    assert get_deletion_date(State.SECOND_EMAIL, start) == D(2023, 3, 27)
    assert get_deletion_date(State.FINAL_EMAIL, start) == D(2023, 3, 24)
    assert get_deletion_date(State.CLEANUP, start) == None
    assert get_deletion_date(State.HOLD, start) == None


@mark.xfail
def test_4th_of_July():
    """
         June 2023
    Su Mo Tu We Th Fr Sa
                 1  2  3
     4  5  6  7  8  9 10
    11 12 13 14 15 16 17
    18 19 20 21 22 23 24
    25  S 27 28 29 30     --> Start

         July 2023
    Su Mo Tu We Th Fr Sa
                       1
    2  3  4  5  6  7  8
    9  10 11 12 13 14 15
    16 17 18 19 20 21 22
    23 24  E 26 27 28 29 --> anticipated deletion date
    30 31"""
    start = D(2023, 6, 26)
    # assert get_deletion_date(start, 0) == start
    # assert get_deletion_date(start, 20) == D(2023, 7, 25)
