from django.views.generic import TemplateView
from utils.mixins import CustomLoginRequiredMixin

from django_filters.views import FilterView
from .models import Shiwake

import logging

logger = logging.getLogger(__name__)

class ShiwakeEntity:
    def __init__(self, shiwake):
        self.shiwake_date = shiwake.shiwake_date

        kanjo_list = shiwake.kanjos.all()
        self.kari_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == True]
        self.kashi_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == False]

        self.kari_amount_sum = sum([kanjo.amount for kanjo in self.kari_kanjo_list])
        self.kashi_amount_sum = sum([kanjo.amount for kanjo in self.kashi_kanjo_list])

# Create your views here.
class ShiwakeListView(CustomLoginRequiredMixin, FilterView):

    model = Shiwake

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """
        return super().get(request, **kwargs)
    
    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        user = self.request.user  # ログインユーザーモデルの取得
        return Shiwake.objects.prefetch_related('kanjos').filter(owner = user).order_by('shiwake_date')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['shiwake_entity_list'] = [ShiwakeEntity(shiwake) for shiwake in context['shiwake_list']]
        return context
