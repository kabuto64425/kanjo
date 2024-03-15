from django.views.generic import TemplateView
from utils.mixins import CustomLoginRequiredMixin

from django_filters.views import FilterView
from .models import Shiwake

class MyClass:
    def __init__(self, name):
        self.name = name            # インスタンス変数

# Create your views here.
class ShiwakeListView(CustomLoginRequiredMixin, FilterView):

    model = Shiwake

    # 1ページの表示
    paginate_by = 10

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """
        return super().get(request, **kwargs)
    
    def get_context_data(self, *, shiwake_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        context = super().get_context_data(shiwake_list=shiwake_list, **kwargs)
        context['shiwake_list'] = [MyClass("test") for shiwake in Shiwake.objects.all()]
        return context
