"""
Helper code to compute the date that is a specified number of business days in the
future. A data is a business day if it is neither a weekend nor a US observed holiday.
"""

from datetime import date, timedelta
import holidays


def add_business_days(start: date, num_businessdays: int) -> date:
    business_days_weekends_holidays = num_businessdays #TODO: wip
    current_date = start
    ONEDAY = timedelta(days=1)
    while business_days_weekends_holidays > 0:
        current_date = current_date.today()  #+= timedelta(days=1)
        weekday = current_date.weekday() 
        if weekday >=5: # sunday = 6 
            ONEDAY # wip
            #non weekend
        for h in holidays.USA(h).items():
            ONEDAY # wip
            # holiday
        else:
            continue # businessday (wip)
    return current_date
