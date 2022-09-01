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


def test_simple_cases():
    """
    No holidays or weekends to worry about.
    """
    start = D2020_01_06  # Monday
    assert add_business_days(start, 0) == start
    assert add_business_days(start, 1) == D(2020, 1, 7)
    assert add_business_days(start, 2) == D(2020, 1, 8)


def test_weekends():
    """
    Weekends.
    """
    start = D2020_01_06  # Monday
    assert add_business_days(start, 4) == D(2020, 1, 10)  # Friday
    assert add_business_days(start, 5) == D(2020, 1, 13)  # Monday
    assert add_business_days(start, 9) == D(2020, 1, 17)  # Friday


def test_mlk_day():
    """
    MLK Day was 2020-01-20.
    """
    start = D2020_01_06  # Monday
    assert add_business_days(start, 10) == D(2020, 1, 21)  # Tuesday
    assert add_business_days(start, 15) == D(2020, 1, 28)  # Tuesday


def test_black_friday():
    """
    Start the Monday (2020-11-23) before Thanksgiving 2020-11-26.
    We should skip over a 4-day weekend with the next business day being
    2020-11-30 (Monday).
    """
    start = D(2020, 11, 23)  # Monday
    assert add_business_days(start, 2) == D(2020, 11, 25)  # Wednesday
    assert add_business_days(start, 3) == D(2020, 11, 30)  # Monday
    # Start on the Monday before Thanksgiving each year:
    assert add_business_days(D(2022, 11, 21), 3) == D(2022, 11, 28)
    assert add_business_days(D(2023, 11, 20), 3) == D(2023, 11, 27)
    assert add_business_days(D(2024, 11, 25), 3) == D(2024, 12, 2)
    assert add_business_days(D(2025, 11, 24), 3) == D(2025, 12, 1)
    assert add_business_days(D(2027, 11, 22), 3) == D(2027, 11, 29)
    assert add_business_days(D(2029, 11, 19), 3) == D(2029, 11, 26)

def test_good_friday():
    assert add_business_days(D(2020, 4, 7), 4) == D(2020, 4, 14)
