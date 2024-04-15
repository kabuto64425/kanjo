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
        
        context['selected'] = period[1]
        context['select_option_list'] = self.create_period_selector_choices()

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
        
        hiyo_zandaka_sum = sum([kanjo["zandaka"] for kanjo in hiyo_list])
        shueki_zandaka_sum = sum([kanjo["zandaka"] for kanjo in shueki_list])

        if hiyo_zandaka_sum > shueki_zandaka_sum:
            sonshitsu = {
                "name" : "当期純損失",
                "zandaka" : hiyo_zandaka_sum - shueki_zandaka_sum,
                "kamoku_type" : MasterKanjoKamokuType.SHUEKI
            }
            shueki_list.append(sonshitsu)
            shueki_zandaka_sum += sonshitsu["zandaka"]
        else:
            rieki = {
                "name" : "当期純利益",
                "zandaka" : shueki_zandaka_sum - hiyo_zandaka_sum,
                "kamoku_type" : MasterKanjoKamokuType.HIYO
            }
            hiyo_list.append(rieki)
            hiyo_zandaka_sum += rieki["zandaka"]
        
        context["hiyo_list"] = hiyo_list
        context["shueki_list"] = shueki_list

        context["hiyo_zandaka_sum"] = hiyo_zandaka_sum
        context["shueki_zandaka_sum"] = shueki_zandaka_sum
        
        return context
        
        