"""
Helper code to compute the date that is a specified number of business days in the
future. A data is a business day if it is neither a weekend nor a US observed holiday.
"""

from datetime import date, timedelta
from tkinter import ON

from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as RD, TH, FR
from holidays.countries.united_states import UnitedStates
from holidays.constants import FRI, SAT, SUN, WEEKEND, JUN, DEC


ONE_DAY = timedelta(days=1)


class HGSCHolidays(UnitedStates):
    def _populate(self, year):
        print("populating", year)
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
        # Add winter break, the period between Christmas and New Year.
        # To be conservative, include on Dec 23 through Jan 2.
        month_days = [(1, 1), (1, 2)] + [(12, d) for d in range(23, 32)]
        for m, d in month_days:
            self.append(date(year, m, d))
        return


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
