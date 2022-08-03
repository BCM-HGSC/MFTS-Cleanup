"""
Helper code to compute the date that is a specified number of business days in the
future. A data is a business day if it is neither a weekend nor a US observed holiday.
"""

from datetime import date, timedelta
import holidays


ONE_DAY = timedelta(days=1)

def add_business_days(start: date, num_businessdays: int) -> date:
    current_date = start
    remaining_business_days = num_businessdays
    us_holidays = holidays.USA()
    while remaining_business_days > 0:
        current_date += ONE_DAY
        if current_date.weekday() >=5: # sunday = 6 
            continue  # weekend, so nothing to do
        if current_date in us_holidays:
            continue # businessday (wip)
        remaining_business_days -= 1
    return current_date
