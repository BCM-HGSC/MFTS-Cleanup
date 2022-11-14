"""
Helper code to compute the date that is a specified number of business days in the
future. A data is a business day if it is neither a weekend nor a US observed holiday.
"""

from datetime import date, timedelta
from dateutil.easter import easter as E
from dateutil.relativedelta import relativedelta as RD
from dateutil.relativedelta import TH, FR

import holidays
from holidays.constants import SAT, SUN, WEEKEND, JUN, DEC


ONE_DAY = timedelta(days=1)


def add_business_days(start: date, num_businessdays: int) -> date:
    current_date = start
    remaining_business_days = num_businessdays
    while remaining_business_days > 0:
        current_date += ONE_DAY
        if current_date.weekday() >= 5:  # sunday = 6
            continue  # weekend, so nothing to do
        if current_date in dep_holidays:
            continue  # working day
        remaining_business_days -= 1
    return current_date


class DepartmentalHolidays(holidays.US):
    def _populate(self, year):
        holidays.US._populate(self, year)
        # Columbus day is not observed
        self.pop_named("Columbus Day")
        # removing Veterans day because we don't observe
        self.pop_named("Veterans Day")
        # observe Good Friday as per hgsc google cal
        self[E(year) + RD(weekday=FR(-1))] = "Good Friday"
        # also observe black friday
        self[date(year, 11, 1) + RD(weekday=TH(+4)) + ONE_DAY] = "Black Friday"
        # Juneteenth Day
        if year > 2022:
            name = "Juneteenth National Independence Day"
            self[date(year, JUN, 19)] = name
            if self.observed and date(year, JUN, 19).weekday() == SAT:
                self[date(year, JUN, 18)] = name + " (Observed)"
            elif self.observed and date(year, JUN, 19).weekday() == SUN:
                self[date(year, JUN, 20)] = name + " (Observed)"
        # Christmas Eve
        if year < 2022:
            name = "Christmas Eve"
            self[date(year, DEC, 24)] = name
            name = name + " (Observed)"
            # If on Friday, observed on Thursday
            if self.observed and date(year, DEC, 24).weekday() == SAT:
                self[date(year, DEC, 24) + RD(days=-1)] = name
            # If on Saturday or Sunday, observed on Friday
            elif self.observed and date(year, DEC, 24).weekday() in WEEKEND:
                self[date(year, DEC, 24) + RD(weekday=FR(-1))] = name


dep_holidays = DepartmentalHolidays()
