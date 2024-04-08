from datetime import date
from datetime import datetime
from datetime import time
from dateutil import relativedelta
from django.utils import timezone

# 次の期末日を求める
def next_last_day(target_date, last_month, last_day):

    current_year = target_date.year
    # 2/29が設定されている場合
    if (last_month, last_day) == (2, 29):
        compare_date = date(current_year, last_month + 1, 1) - relativedelta.relativedelta(days=1)
        if target_date > compare_date:
            return (compare_date + relativedelta.relativedelta(years=1)) + relativedelta.relativedelta(months=1, day=1) - relativedelta.relativedelta(days=1)
        else:
            return compare_date
    
    compare_date = date(current_year, last_month, last_day)

    if target_date > compare_date:
        return compare_date + relativedelta.relativedelta(years=1)
    else:
        return compare_date

# 該当する期間を見つける
# タプル形式
# index 0: 期首
# index 1: 期末
def find_peripd(target_date, last_month, last_day):
    current_year = target_date.year

    # 2/29が設定されている場合
    # うるう日のため別で処理
    if (last_month, last_day) == (2, 29):
        # 「対象年と同じ年の決算日」と比較して、いつの期間に該当するかを調べる
        compare_date = datetime(current_year, last_month + 1, 1) - relativedelta.relativedelta(days=1)
        # 比較できるようにするため
        compare_date = timezone.make_aware(compare_date)
        if target_date > compare_date:
            #「対象年と同じ年の決算日(比較日)」より後の場合、
            # うるう年も考慮して、下記の計算で求める
            # 期末:比較日の次の年の、次の月初の前日(決算月の月末)
            period_last_date = compare_date + relativedelta.relativedelta(years=1, months=1, day=1) - relativedelta.relativedelta(days=1)
            # 期首:期末の1年前の、次の月の1日(決算月の次月初日)
            period_first_date = period_last_date + relativedelta.relativedelta(years=-1, months=1, day=1)
            return (period_first_date, period_last_date)
        else:
            # 「対象年と同じ年の決算日(比較日)」以前の場合、
            # うるう年も考慮して、下記の計算で求める
            # 期末:比較日
            period_last_date = compare_date
            # 期首:期末の1年前の、次の月の1日(決算月の次月初日)
            period_first_date = period_last_date + relativedelta.relativedelta(years=-1, months=1, day=1)
            return (period_first_date, period_last_date)
    
    #「対象年と同じ年の決算日」と比較して、いつの期間に該当するかを調べる
    compare_date = datetime(current_year, last_month, last_day)
    # 比較できるようにするため
    compare_date = timezone.make_aware(compare_date)
    if target_date > compare_date:
        # 「対象年と同じ年の決算日(比較日)」より後の場合、
        # 期末:比較日の次の年の決算日
        period_last_date = compare_date + relativedelta.relativedelta(years=1)
        # 期首:比較日の1年前の次の日
        period_first_date = period_last_date - relativedelta.relativedelta(years=1, days=-1)
        return (period_first_date, period_last_date)
    else:
        # 「対象年と同じ年の決算日(比較日)」以前の場合、
        # 期末:比較日
        period_last_date = compare_date
        # 期首:比較日の1年前の次の日
        period_first_date = period_last_date - relativedelta.relativedelta(years=1, days=-1)
        return (period_first_date, period_last_date)

# 該当する期間を見つける(「見つけたい期間の末日の年」を引数に指定する形式)
# タプル形式
# index 0: 期首
# index 1: 期末
def find_period_from_year(target_year, last_month, last_day):
    if (last_month, last_day) == (2, 29):
        find_date = datetime(target_year, last_month + 1, 1) - relativedelta.relativedelta(days=1)
        return find_peripd(timezone.make_aware(find_date, time()))
    else:
        return find_peripd(timezone.make_aware(datetime.combine(datetime(target_year, last_month, last_day), time())), last_month, last_day)