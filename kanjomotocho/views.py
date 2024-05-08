from django.db.models import Sum, Case, When, Value, IntegerField, F
from django.db.models import Prefetch
from django.views.generic import TemplateView
from utils.mixins import AccountingPeriodLoginRequiredMixin
from shiwake.models import Kanjo, Shiwake
from app.models import MasterKanjoKamoku
from app.models import MasterKanjoKamokuType
# Create your views here.

import logging
import itertools

logger = logging.getLogger(__name__)

class KanjoMotochoView(AccountingPeriodLoginRequiredMixin, TemplateView):
    template_name = "kanjo_motocho/kanjo_motocho.html"

    # 適用のリストを貸方、借方それぞれ作成。dict型で返す
    def build_tekiyo_list(self, target_kanjo_kamoku):
        if not target_kanjo_kamoku:
            return {
                "kari_tekiyo_list" : [],
                "kashi_tekiyo_list" : [],
            }
        kari_tekiyo_list = []
        kashi_tekiyo_list = []

        target_kanjo_kamoku_id = target_kanjo_kamoku.id

        user = self.request.user  # ログインユーザーモデルの取得
        period_from_queryparam = self.find_period_from_queryparam("last_day")

        if target_kanjo_kamoku.kamoku_type in [MasterKanjoKamokuType.SHISAN, MasterKanjoKamokuType.FUSAI, MasterKanjoKamokuType.JUNSHISAN]:
            a = Kanjo.objects.select_related('shiwake').select_related('kanjo_kamoku').filter(**{
                "kanjo_kamoku__id": target_kanjo_kamoku_id,
                "shiwake__shiwake_date__lt": period_from_queryparam[0]
            })
            pre_kari_zan = sum([b.amount for b in a if b.taishaku])
            pre_kashi_zan = sum([b.amount for b in a if not b.taishaku])

            if pre_kari_zan > pre_kashi_zan:
                kari_tekiyo_list.append({
                    "date" : period_from_queryparam[0],
                    "name" : "前期繰越",
                    "amount" : pre_kari_zan - pre_kashi_zan
                })
            elif pre_kari_zan < pre_kashi_zan:
                kashi_tekiyo_list.append({
                    "date" : period_from_queryparam[0],
                    "name" : "前期繰越",
                    "amount" : pre_kashi_zan - pre_kari_zan
                })

            logger.info(sum([b.amount for b in a if b.taishaku]))
            logger.info(sum([b.amount for b in a if not b.taishaku]))

        shiwake_id_dictionaries = Kanjo.objects.select_related('shiwake').select_related('kanjo_kamoku').filter(**{"kanjo_kamoku__id" : target_kanjo_kamoku_id}).values(
            #valuesを使用すると、クエリ実行結果はdict型のリストになる
            "shiwake_id"
        ).distinct()

        shiwakes = Shiwake.objects.prefetch_related(Prefetch('shiwake_kanjos', to_attr='kanjo_prefetched',queryset=Kanjo.objects.select_related('kanjo_kamoku'))).filter(**{
            "owner" : user,
            "shiwake_date__gte": period_from_queryparam[0],
            "shiwake_date__lte": period_from_queryparam[1],
            "id__in" : [elm["shiwake_id"] for elm in shiwake_id_dictionaries]
        }).order_by('shiwake_date')

        for shiwake in shiwakes:
            # 借方
            # 「貸借と勘定科目が一致する勘定」でグループ化。グループ化後にグループごとのamountを合計した値を持たせた配列を出力
            kanjo_list = [(k, sum([elm.amount for elm in g])) for k, g in itertools.groupby(shiwake.kanjo_prefetched, key=lambda kanjo:(kanjo.taishaku, kanjo.kanjo_kamoku))]

            kari_kanjo_list = list(filter(lambda kanjo: kanjo[0][0], kanjo_list))

            kashi_kanjo_list = list(filter(lambda kanjo: not kanjo[0][0], kanjo_list))

            kari_target_kanjo_list = list(filter(lambda kanjo: kanjo[0][1].id==target_kanjo_kamoku_id, kari_kanjo_list))

            if kari_target_kanjo_list:
                # グルーピングしているので、1つしか要素がないはず
                if len(kari_target_kanjo_list) >= 2:
                    logging.warning("1つしか要素がないはずなのに複数見つかりました。")
                kari_target = kari_target_kanjo_list[0]
                # 相手方の勘定リスト0はないはずだけど念のため「諸口」となるようにしておく
                if len(kashi_kanjo_list) != 1:
                    kari_tekiyo_list.append({
                        "date" : shiwake.shiwake_date,
                        "name" : "諸口",
                        "amount" : kari_target[1]
                    })
                else:
                    kari_tekiyo_list.append({
                        "date" : shiwake.shiwake_date,
                        "name" : kashi_kanjo_list[0][0][1],
                        "amount" : kari_target[1]
                    })
                    pass
            
            kashi_target_kanjo_list = list(filter(lambda kanjo: kanjo[0][1].id==target_kanjo_kamoku_id, kashi_kanjo_list))

            if kashi_target_kanjo_list:
                # グルーピングしているので、1つしか要素がないはず
                if len(kashi_target_kanjo_list) >= 2:
                    logging.warning("1つしか要素がないはずなのに複数見つかりました。")
                kashi_target = kashi_target_kanjo_list[0]
                # 相手方の勘定リスト0はないはずだけど念のため「諸口」となるようにしておく
                if len(kari_kanjo_list) != 1:
                    kashi_tekiyo_list.append({
                        "date" : shiwake.shiwake_date,
                        "name" : "諸口",
                        "amount" : kashi_target[1]
                    })
                else:
                    kashi_tekiyo_list.append({
                        "date" : shiwake.shiwake_date,
                        "name" : kari_kanjo_list[0][0][1],
                        "amount" : kashi_target[1]
                    })
                    pass
        
        settlement_tekiyo_name = ""
        if target_kanjo_kamoku.kamoku_type in [MasterKanjoKamokuType.SHISAN, MasterKanjoKamokuType.FUSAI, MasterKanjoKamokuType.JUNSHISAN]:
            settlement_tekiyo_name = "次期繰越"
        elif target_kanjo_kamoku.kamoku_type in [MasterKanjoKamokuType.HIYO, MasterKanjoKamokuType.SHUEKI]:
            settlement_tekiyo_name = "損益"

        kari_sum = sum([kari_tekiyo["amount"] for kari_tekiyo in kari_tekiyo_list])
        kashi_sum = sum([kashi_tekiyo["amount"] for kashi_tekiyo in kashi_tekiyo_list])
        if kari_sum > kashi_sum:
            kashi_tekiyo_list.append({
                "date" : period_from_queryparam[1],
                "name" : settlement_tekiyo_name,
                "amount" : kari_sum - kashi_sum
            })
        elif kari_sum < kashi_sum:
            kari_tekiyo_list.append({
                "date" : period_from_queryparam[1],
                "name" : settlement_tekiyo_name,
                "amount" : kashi_sum - kari_sum
            })

        return {
            "kari_tekiyo_list" : kari_tekiyo_list,
            "kashi_tekiyo_list" : kashi_tekiyo_list,
        }

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        
        period_from_queryparam = self.find_period_from_queryparam("last_day")

        context['selected'] = period_from_queryparam[1]
        context['select_option_list'] = self.create_period_selector_choices()

        target_kanjo_kamoku_id = None

        if self.request.GET.get("target_kanjo_kamoku") is not None:
            try:
                target_kanjo_kamoku_id = int(self.request.GET.get("target_kanjo_kamoku"))  # 文字列を実際にint関数で変換してみる
            except ValueError:
                pass
        
        context['target_kanjo_kamoku_id'] = target_kanjo_kamoku_id

        target_kanjo_kamoku = None
        target_kanjo_kamoku_name = ""
        if target_kanjo_kamoku_id:
            try:
                target_kanjo_kamoku = MasterKanjoKamoku.objects.get(id=target_kanjo_kamoku_id)
                target_kanjo_kamoku_name = target_kanjo_kamoku.name
            except MasterKanjoKamoku.DoesNotExist:
                 pass
        context['target_kanjo_kamoku_name'] = target_kanjo_kamoku_name

        master_kanjo_kamokus = MasterKanjoKamoku.objects.all()
        kanjo_kamoku_choices = [(None, "")]
        kanjo_kamoku_choices += [(master_kanjo_kamoku.id, master_kanjo_kamoku) for master_kanjo_kamoku in master_kanjo_kamokus]

        context['kanjo_kamoku_option_list'] = kanjo_kamoku_choices

        tekiyo_list = self.build_tekiyo_list(target_kanjo_kamoku)
        
        context["kari_tekiyo_list"] = tekiyo_list["kari_tekiyo_list"]
        context["kashi_tekiyo_list"] = tekiyo_list["kashi_tekiyo_list"]

        context["kari_sum"] = sum([kari_tekiyo["amount"] for kari_tekiyo in tekiyo_list["kari_tekiyo_list"]])
        context["kashi_sum"] = sum([kashi_tekiyo["amount"] for kashi_tekiyo in tekiyo_list["kashi_tekiyo_list"]])
        return context
        
        