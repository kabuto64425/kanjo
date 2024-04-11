from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from utils import common
from django.db.models import Max,Min
from datetime import datetime, time

from shiwake.models import Shiwake

class CustomLoginRequiredMixin(LoginRequiredMixin):
    def handle_no_permission(self):
        if self.raise_exception or self.request.user.is_authenticated:
            return super().handle_no_permission()
        else:
            return redirect(self.get_login_url())

class AccountingPeriodLoginRequiredMixin(CustomLoginRequiredMixin):
    # クエリパラメータに渡された日時から、該当の期間を算出する
    # param_key: 対象となるクエリパラメータのキー(値が'%Y-%m-%d'形式のもの)
    def find_period_from_queryparam(self, param_key):
        user = self.request.user  # ログインユーザーモデルの取得
        query_last_day = self.request.GET.get(param_key)

        if query_last_day:
            target = timezone.make_aware(datetime.strptime(query_last_day, '%Y-%m-%d'))
            return common.find_peripd(target, user.last_month, user.last_day)
        else:
            return common.find_peripd(timezone.now(), user.last_month, user.last_day)
    
    # ログインユーザーの仕訳情報から、会計期間絞り込み用の選択肢候補リストを作成する
    # 「仕訳日が最も早い日」「仕訳日が最も遅い日」「今日」の全てが含まれる期間を
    # 決算日ごとの1年区切りでリストにして返す
    # リストの各要素は各会計期間の(期首日, 期末日)のタプル形式
    def create_period_selector_choices(self):
        user = self.request.user  # ログインユーザーモデルの取得

        # 所有している仕訳の一番早い日と一番遅い日を取得
        aggreate_shiwake_date = Shiwake.objects.filter(owner=user).aggregate(Max("shiwake_date"), Min("shiwake_date"))

        candidate_dates = []
        for date in [aggreate_shiwake_date["shiwake_date__max"], aggreate_shiwake_date["shiwake_date__min"], timezone.now().date()]:
            if date:
                candidate_dates.append(date)
        
        candidate_datetimes = [timezone.make_aware(datetime.combine(date, time())) for date in candidate_dates]

        periods = [common.find_peripd(candidate_datetime, user.last_month, user.last_day) for candidate_datetime in candidate_datetimes]

        last_day_of_earliest = min(periods)[1]
        last_day_of_latest = max(periods)[1]

        select_options = []

        for current_year in range(last_day_of_earliest.year, last_day_of_latest.year + 1):
            select_options.append(common.find_period_from_year(current_year, user.last_month, user.last_day))

        return select_options