from datetime import date as D

from mftscleanup.business_days import add_business_days, HGSCHolidays


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


def test_calendar_2019():
    """
    2019-01-01 New Year's Day
    2019-01-21 Martin Luther King Jr. Day
    2019-02-18 Washington's Birthday
    2019-04-19 Good Friday
    2019-05-27 Memorial Day
    2019-07-04 Independence Day
    2019-09-02 Labor Day
    2019-11-28 Thanksgiving
    2019-11-29 Black Friday
    2019-12-24 Christmas Eve
    2019-12-25 Christmas Day
    """
    dates = set(HGSCHolidays(years=2019))
    assert dates == set(
        [
            D(2019, 1, 1),
            D(2019, 1, 21),
            D(2019, 2, 18),
            D(2019, 4, 19),
            D(2019, 5, 27),
            D(2019, 7, 4),
            D(2019, 9, 2),
            D(2019, 11, 28),
            D(2019, 11, 29),
            D(2019, 12, 24),
            D(2019, 12, 25),
        ]
    )


def test_calendar_2020():
    """
    2020-01-01 New Year's Day
    2020-01-20 Martin Luther King Jr. Day
    2020-02-17 Washington's Birthday
    2020-04-10 Good Friday
    2020-05-25 Memorial Day
    2020-07-03 Independence Day (Observed)
    2020-07-04 Independence Day
    2020-09-07 Labor Day
    2020-11-26 Thanksgiving
    2020-11-27 Black Friday
    2020-12-24 Christmas Eve
    2020-12-25 Christmas Day
    """
    dates = set(HGSCHolidays(years=2020))
    assert dates == set(
        [
            D(2020, 1, 1),
            D(2020, 1, 20),
            D(2020, 2, 17),
            D(2020, 4, 10),
            D(2020, 5, 25),
            D(2020, 7, 3),
            D(2020, 7, 4),
            D(2020, 9, 7),
            D(2020, 11, 26),
            D(2020, 11, 27),
            D(2020, 12, 24),
            D(2020, 12, 25),
        ]
    )


def test_calendar_2022():
    """
    2020-01-01 New Year's Day
    2020-01-20 Martin Luther King Jr. Day
    2020-02-17 Washington's Birthday
    2020-04-10 Good Friday
    2020-05-25 Memorial Day
    2020-07-03 Independence Day (Observed)
    2020-07-04 Independence Day
    2020-09-07 Labor Day
    2020-11-26 Thanksgiving
    2020-11-27 Black Friday
    2020-12-24 Christmas Eve
    2020-12-25 Christmas Day
    """
    dates = set(HGSCHolidays(years=2022))
    assert dates == set(
        [
            D(2022, 1, 1),
            D(2022, 1, 17),
            D(2022, 2, 21),
            D(2022, 4, 15),
            D(2022, 5, 30),
            D(2022, 6, 19),
            D(2022, 6, 20),
            D(2022, 7, 4),
            D(2022, 9, 5),
            D(2022, 11, 24),
            D(2022, 11, 25),
            D(2022, 12, 23),
            D(2022, 12, 24),
            D(2022, 12, 25),
            D(2022, 12, 26),
        ]
    )


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
    # Test 2020-11-05:
    start = D(2020, 11, 5)  # Thursday
    assert add_business_days(start, 1) == D(2020, 11, 6)  # Friday
    assert add_business_days(start, 4) == D(2020, 11, 11)  # Wednesday
    assert add_business_days(start, 5) == D(2020, 11, 12)  # Thursday
    assert add_business_days(start, 10) == D(2020, 11, 19)  # Thursday
    # Start on the Monday before Thanksgiving each year:
    assert add_business_days(D(2022, 11, 21), 3) == D(2022, 11, 28)
    assert add_business_days(D(2023, 11, 20), 3) == D(2023, 11, 27)
    assert add_business_days(D(2024, 11, 25), 3) == D(2024, 12, 2)
    assert add_business_days(D(2025, 11, 24), 3) == D(2025, 12, 1)
    assert add_business_days(D(2027, 11, 22), 3) == D(2027, 11, 29)
    assert add_business_days(D(2029, 11, 19), 3) == D(2029, 11, 26)


def test_good_friday():
    """
        April 2020
    Su Mo Tu We Th Fr Sa
              1  2  3  4
     5  6  7  8  9 GF 11  <- Good Friday was April 10, 2020
    12 13 14 15 16 17 18
    19 20 21 22 23 24 25
    26 27 28 29 30
    """
    assert add_business_days(D(2020, 4, 7), 4) == D(2020, 4, 14)
    assert add_business_days(D(2020, 4, 9), 1) == D(2020, 4, 13)


"""
      May 2020
Su Mo Tu We Th Fr Sa
                1  2
 3  4  5  6  7  8  9
10 11 12 13 14 15 16
17 18 19 20 21 ST 23
24 25 26 27 28 MD 30
31

     June 2020
Su Mo Tu We Th Fr Sa
    1  2  3  4  5  6
 7  8  9 10 11 12 13
14 15 16 SE 18 JT 20
21 22 23 24 25 26 27
28 29 30
"""


def test_Juneteenth_2020():
    assert add_business_days(D(2020, 5, 22), 15) == D(2020, 6, 15)  # first email test
    assert add_business_days(D(2020, 6, 15), 3) == D(2020, 6, 18)  # second email test
    assert add_business_days(D(2020, 6, 18), 3) == D(2020, 6, 23)  # Final email test
    assert add_business_days(D(2020, 6, 23), 1) == D(2020, 6, 24)  # cleanup


#   2021 & 2022 Juneteenth fall on Sat and Sun. Next test will be for 2023. Memorial day falls on May 29th

"""
      May 2023
Su Mo Tu We Th Fr Sa
    1  2  3  4  5  6
 7  8  9 10 11 12 13
14 15 16 17 18 19 20
21 22 23 24 25 26 27
28 MD 30 31

     June 2023
Su Mo Tu We Th Fr Sa
             1  2  3
 4  5  6  7  8  9 10
11 12 13 14 15 16 17
18 JT 20 21 22 23 24
25 26 27 28 29 30
"""


def test_Juneteenth_2023():
    # ticket starts on 5/22/2023
    assert add_business_days(D(2023, 6, 12), 5) == D(2023, 6, 20)  # first email
    assert add_business_days(D(2023, 6, 20), 3) == D(2023, 6, 23)  # second email


def test_no_columbus_day_2022():
    """
        October 2022
    Su Mo Tu We Th Fr Sa
                       1
     2  3  4  5  6  7  8
     9 CD 11 12 13 14 15 <- Oct 10 should be a business day.
    16 17 18 19 20 21 22
    23 24 25 26 27 28 29
    30 31
    """
    assert add_business_days(D(2022, 10, 7), 1) == D(2022, 10, 10)
