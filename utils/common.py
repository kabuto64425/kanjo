from datetime import date
from dateutil import relativedelta

# 次の期末日を求める
def next_last_day(target_date, last_month, last_day):

    current_year = target_date.year
    compare_date = date(current_year, last_month, last_day)
    if target_date > compare_date:
        return compare_date + relativedelta.relativedelta(years=1)
    else:
        return compare_date