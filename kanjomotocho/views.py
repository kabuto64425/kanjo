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
        
        