"""
Helper code to compute the date that is a specified number of business days in the
future. A data is a business day if it is neither a weekend nor a US observed holiday.
"""

from datetime import date, timedelta


ONE_DAY = timedelta(days=1)

def add_business_days(start: date, num_businessdays: int) -> date:
    raise NotImplementedError  # TODO
