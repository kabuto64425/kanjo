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

    # 貸借対象表のデータを作成
    def create_taishaku_context_data(self, period):
        user = self.request.user  # ログインユーザーモデルの取得
        filters = {
            "shiwake__owner" : user,
            "shiwake__shiwake_date__lte": period[1],
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
        
        shisan_list = []
        fusai_list = []
        junshisan_list = []

        kurikosi_rieki_joyokin_zandaka = 0
        soneki = 0
        
        for kanjo in qs:
            if kanjo["kamoku_type"] == MasterKanjoKamokuType.SHISAN:
                shisan_list.append(kanjo)
            elif kanjo["kamoku_type"] == MasterKanjoKamokuType.FUSAI:
                kanjo["zandaka"] *= -1
                fusai_list.append(kanjo)
            elif kanjo["kamoku_type"] == MasterKanjoKamokuType.JUNSHISAN:
                if kanjo["kanjo_kamoku__name"] == "繰越利益剰余金":
                    kurikosi_rieki_joyokin_zandaka -= kanjo["zandaka"]
                else :
                    kanjo["zandaka"] *= -1
                    junshisan_list.append(kanjo)
            elif kanjo["kamoku_type"] == MasterKanjoKamokuType.HIYO:
                soneki -= kanjo["zandaka"]
            elif kanjo["kamoku_type"] == MasterKanjoKamokuType.SHUEKI:
                soneki -= kanjo["zandaka"]
        
        kurikosi_rieki_joyokin_zandaka += soneki
        junshisan_list.append({
            "name" : "繰越利益剰余金",
            "zandaka" : kurikosi_rieki_joyokin_zandaka,
            "kamoku_type" : MasterKanjoKamokuType.JUNSHISAN
        })
        
        kari_zandaka_sum = sum([kanjo["zandaka"] for kanjo in shisan_list])
        kashi_zandaka_sum = sum([kanjo["zandaka"] for kanjo in fusai_list]) + sum([kanjo["zandaka"] for kanjo in junshisan_list])
        
        return {
            "shisan_list" : shisan_list,
            "fusai_list" : fusai_list,
            "junshisan_list" : junshisan_list,
            "kari_zandaka_sum" : kari_zandaka_sum,
            "kashi_zandaka_sum" : kashi_zandaka_sum,
        }

    # 損益計算書のデータを作成
    def create_soneki_context_data(self, period):
        user = self.request.user  # ログインユーザーモデルの取得
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
        
        return {
            "hiyo_list" : hiyo_list,
            "shueki_list" : shueki_list,
            "hiyo_zandaka_sum" : hiyo_zandaka_sum,
            "shueki_zandaka_sum" : shueki_zandaka_sum,
        }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        period = self.find_period_from_queryparam("last_day")
        
        context['selected'] = period[1]
        context['select_option_list'] = self.create_period_selector_choices()

        # 貸借対照表
        context.update(self.create_taishaku_context_data(period))

        # 損益計算書
        context.update(self.create_soneki_context_data(period))
        
        return context
        
        