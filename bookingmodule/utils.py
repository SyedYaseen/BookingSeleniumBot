from datetime import date, datetime
from dateutil import relativedelta


def months_calc(start_date, return_date):
    current_date = date.today()

    # convert string to date object
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    return_date = datetime.strptime(return_date, "%Y-%m-%d")

    # Get the relative delta between two dates
    start_delta = relativedelta.relativedelta(start_date, current_date)
    return_delta = relativedelta.relativedelta(return_date, current_date)

    # get months difference
    start_months = start_delta.months + (start_delta.years * 12)
    return_months = return_delta.months + (return_delta.years * 12)

    return {"start_months": start_months, "return_months": return_months}
