from django.db.models import Sum, Case, When, Value, IntegerField, F
from django.views.generic import TemplateView
from utils.mixins import AccountingPeriodLoginRequiredMixin
from shiwake.models import Kanjo
from app.models import MasterKanjoKamokuType
# Create your views here.

import logging

logger = logging.getLogger(__name__)

class TaishakuSonekiView(AccountingPeriodLoginRequiredMixin, TemplateView):
    template_name = "zaimu/taishaku_soneki.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        user = self.request.user  # ログインユーザーモデルの取得
        period = self.find_period_from_queryparam("last_day")

        filters = {
            "shiwake__owner" : user,
            "shiwake__shiwake_date__gte": period[0],
            "shiwake__shiwake_date__lte": period[1],
            "kanjo_kamoku__kamoku_type__in": [MasterKanjoKamokuType.HIYO, MasterKanjoKamokuType.SHUEKI]
        }
        
        qs = Kanjo.objects.select_related('shiwake').select_related('kanjo_kamoku').annotate(
                # 借方なら+amount
                # 貸方なら-amount
                # を保存する列taishaku_amount
                taishaku_amount = Case(
                    When(taishaku=True, then=F("amount")),
                    default=-F("amount")
                )
            ).filter(**filters).values(
                #valuesを使用すると、クエリ実行結果はdict型のリストになる
                "kanjo_kamoku", "kanjo_kamoku__name", "kanjo_kamoku__kamoku_type"
            ).annotate(
                # taishaku_amountを勘定科目ごとで集計した列zandaka
        	    zandaka = Sum('taishaku_amount'),
                name = F("kanjo_kamoku__name"),
                kamoku_type = F("kanjo_kamoku__kamoku_type")
            )
                
        hiyo_list = []
        shueki_list = []

        for kanjo in qs:
            if kanjo["kamoku_type"] == MasterKanjoKamokuType.HIYO:
                hiyo_list.append(kanjo)
            elif kanjo["kamoku_type"] == MasterKanjoKamokuType.SHUEKI:
                kanjo["zandaka"] *= -1
                shueki_list.append(kanjo)
        
        context["hiyo_list"] = hiyo_list
        context["shueki_list"] = shueki_list
        
        return context
        
        