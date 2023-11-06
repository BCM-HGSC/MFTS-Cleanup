"""
Helper code to compute the date that is a specified number of business days in the
future. A data is a business day if it is neither a weekend nor a US observed holiday.
"""

from datetime import date, timedelta

from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as RD, TH, FR
from holidays.countries.united_states import UnitedStates
from holidays.constants import FRI, SAT, SUN, WEEKEND, JUN, DEC


ONE_DAY = timedelta(days=1)


class HGSCHolidays(UnitedStates):
    def _populate(self, year):
        # Populate the holiday list with the default US holidays.
        super()._populate(year)
        # Remove holidays not observed at HGSC.
        self.pop_named("Columbus Day")
        self.pop_named("Veterans Day")
        # Add extra HGSC FTO days.
        # Use the formula from the holidays source code for provincial Good Friday:
        self[easter(year) + RD(weekday=FR(-1))] = "Good Friday"
        # Juneteenth Day
        # The US started celebrating Juneteenth in 2021, but HGSC started in 2022.
        if year > 2022:
            name = "Juneteenth National Independence Day"
            self[date(year, JUN, 19)] = name
            if date(year, JUN, 19).weekday() == SAT:
                self[date(year, JUN, 18)] = name + " (Observed)"
            elif date(year, JUN, 19).weekday() == SUN:
                self[date(year, JUN, 20)] = name + " (Observed)"
        # Use the formula for Thanksgiving and add one day:
        self[date(year, 11, 1) + RD(weekday=TH(+4)) + ONE_DAY] = "Black Friday"
        # Christmas Eve
        # HGSC celebrated Christmas Eve before 2022, but not in 2022 or 2023 when it
        # fell on a weekend.
        # It is unclear what the future will hold regarding Christmas Eve.
        # It could be that the Christmas Eve had to be sacrificed to obtain Juneteenth.
        # We will treat Christmas Eve and observed Christmas Eve as a
        # non-business day to be conservative.
        name = "Christmas Eve"
        self[date(year, DEC, 24)] = name
        name = name + " (Observed)"
        # If on Friday, observed on Thursday (the 23rd)
        if date(year, DEC, 24).weekday() == FRI:
            self[date(year, DEC, 23)] = name
        # If on Saturday or Sunday, observed on Friday
        elif date(year, DEC, 24).weekday() in WEEKEND:
            self[date(year, DEC, 24) + RD(weekday=FR(-1))] = name


hgsc_holidays = HGSCHolidays()


def add_business_days(start: date, num_businessdays: int) -> date:
    current_date = start
    remaining_business_days = num_businessdays
    while remaining_business_days > 0:
        current_date += ONE_DAY
        if current_date.weekday() >= 5:  # sunday = 6
            continue  # weekend, so nothing to do
        if current_date in hgsc_holidays:
            continue  # businessday
        remaining_business_days -= 1
    return current_date
