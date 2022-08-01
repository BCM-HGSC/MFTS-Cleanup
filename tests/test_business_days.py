from datetime import date as D 

from pytest import mark

from mftscleanup.business_days import add_business_days


"""
For reference:
$ cal 1 2020
    January 2020
Su Mo Tu We Th Fr Sa
          1  2  3  4
 5  6  7  8  9 10 11
12 13 14 15 16 17 18
19 20 21 22 23 24 25
26 27 28 29 30 31
"""

D2020_01_06 = D(2020, 1, 6)  # Monday


def test_simple_date_works_as_expected():
    """
    Making sure we understand correctly.
    """
    assert D(2020, 1, 6).weekday() == 0  # Monday
    assert D(2020, 1, 10).weekday() == 4  # Friday
    assert D(2020, 1, 12).weekday() == 6  # Sunday
    assert D(2020, 1, 12).strftime("%a") == "Sun"  # Sunday


@mark.xfail
def test_simple_cases():
    """
    No holidays or weekends to worry about.
    """
    start = D2020_01_06  # Monday
    assert add_business_days(start, 0) == start
    assert add_business_days(start, 1) == D(2020, 1, 7)
    assert add_business_days(start, 2) == D(2020, 1, 8)


@mark.xfail
def test_weekends():
    """
    Weekends.
    """
    start = D2020_01_06  # Monday
    assert add_business_days(start, 4) == D(2020, 1, 10)  # Friday
    assert add_business_days(start, 5) == D(2020, 1, 13)  # Monday
    assert add_business_days(start, 9) == D(2020, 1, 17)  # Friday


@mark.xfail
def test_mlk_day():
    """
    MLK Day was 2020-01-20.
    """
    start = D2020_01_06  # Monday
    assert add_business_days(start, 10) == D(2020, 1, 21)  # Tuesday
    assert add_business_days(start, 15) == D(2020, 1, 28)  # Tuesday
