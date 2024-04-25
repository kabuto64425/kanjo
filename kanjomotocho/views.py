from django.db.models import Sum, Case, When, Value, IntegerField, F
from django.db.models import Prefetch
from django.views.generic import TemplateView
from utils.mixins import AccountingPeriodLoginRequiredMixin
from shiwake.models import Kanjo, Shiwake
from app.models import MasterKanjoKamokuType
# Create your views here.

import logging
import itertools

logger = logging.getLogger(__name__)

class KanjoMotochoView(AccountingPeriodLoginRequiredMixin, TemplateView):
    template_name = "kanjo_motocho/kanjo_motocho.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        d = Kanjo.objects.select_related('shiwake').select_related('kanjo_kamoku').filter(**{"kanjo_kamoku__name" : "売掛金"}).values(
                #valuesを使用すると、クエリ実行結果はdict型のリストになる
                "shiwake_id"
            ).distinct()
        
        shiwakes = Shiwake.objects.prefetch_related(Prefetch('shiwake_kanjos', to_attr='kanjo_prefetched',queryset=Kanjo.objects.select_related('kanjo_kamoku'))).filter(**{
            "id__in" : [elm["shiwake_id"] for elm in d]
        }).order_by('shiwake_date')

        kari_tekiyo_list = []
        kashi_tekiyo_list = []

        for shiwake in shiwakes:
            # 借方
            # 「貸借と勘定科目が一致する勘定」でグループ化。グループ化後にグループごとのamountを合計した値を持たせた配列を出力
            kanjo_list = [(k, sum([elm.amount for elm in g])) for k, g in itertools.groupby(shiwake.kanjo_prefetched, key=lambda kanjo:(kanjo.taishaku, kanjo.kanjo_kamoku))]

            kari_kanjo_list = list(filter(lambda kanjo: kanjo[0][0], kanjo_list))

            kashi_kanjo_list = list(filter(lambda kanjo: not kanjo[0][0], kanjo_list))

            kari_target_kanjo_list = list(filter(lambda kanjo: kanjo[0][1].name=="売掛金", kari_kanjo_list))

            if kari_target_kanjo_list:
                # グルーピングしているので、1つしか要素がないはず
                if len(kari_target_kanjo_list) >= 2:
                    logging.warning("1つしか要素がないはずなのに複数見つかりました。")
                kari_target = kari_target_kanjo_list[0]
                # 相手方の勘定リスト0はないはずだけど念のため「諸口」となるようにしておく
                if len(kashi_kanjo_list) != 1:
                    kari_tekiyo_list.append({
                        "name" : "諸口",
                        "amount" : kari_target[1]
                    })
                else:
                    kari_tekiyo_list.append({
                        "name" : kashi_kanjo_list[0][0][1],
                        "amount" : kari_target[1]
                    })
                    pass
            
            kashi_target_kanjo_list = list(filter(lambda kanjo: kanjo[0][1].name=="売掛金", kashi_kanjo_list))

            if kashi_target_kanjo_list:
                # グルーピングしているので、1つしか要素がないはず
                if len(kashi_target_kanjo_list) >= 2:
                    logging.warning("1つしか要素がないはずなのに複数見つかりました。")
                kashi_target = kashi_target_kanjo_list[0]
                # 相手方の勘定リスト0はないはずだけど念のため「諸口」となるようにしておく
                if len(kari_kanjo_list) != 1:
                    kashi_tekiyo_list.append({
                        "name" : "諸口",
                        "amount" : kashi_target[1]
                    })
                else:
                    kashi_tekiyo_list.append({
                        "name" : kari_kanjo_list[0][0][1],
                        "amount" : kashi_target[1]
                    })
                    pass
        
        context["kari_tekiyo_list"] = kari_tekiyo_list
        context["kashi_tekiyo_list"] = kashi_tekiyo_list
        return context

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
        
        context['selected_start'] = period[0]
        context['selected_end'] = period[1]
        context['select_option_list'] = self.create_period_selector_choices()

        # 貸借対照表
        context.update(self.create_taishaku_context_data(period))

        # 損益計算書
        context.update(self.create_soneki_context_data(period))
        
        return context
        
        