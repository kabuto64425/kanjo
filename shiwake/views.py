from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import FormView
from django.db import transaction
from utils.mixins import CustomLoginRequiredMixin

from django.views.generic.edit import CreateView, UpdateView ,DeleteView
from extra_views import InlineFormSetFactory, CreateWithInlinesView, UpdateWithInlinesView
from django_filters.views import FilterView
from .models import Shiwake, Kanjo
from .forms import ShiwakeForm, ShiwakeForm_temp2, TestForm
from config.consts import KANJO_ROWS

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Row, Column, Layout

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
    
class Child1Inline(InlineFormSetFactory):
    model = Kanjo
    fields = '__all__'
    factory_kwargs = {'extra': 5,'can_order': False, 'can_delete': False}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('kanjo_kamoku', css_class='form-group col-md-6 mb-0'),)
        )

class Child2Inline(InlineFormSetFactory):
    model = Kanjo
    fields = '__all__'
    factory_kwargs = {'extra': 5,'can_order': False, 'can_delete': False}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(Column('kanjo_kamoku', css_class='form-group col-md-6 mb-0'),)
        )

class TestFormView(FormView):
    # テンプレート名の設定
    template_name = 'shiwake/shiwake_form.html'
    # フォームの設定
    form_class = TestForm
    success_url = reverse_lazy('shiwake_list')
    def form_valid(self, form):
        with transaction.atomic():
            shiwake = Shiwake()
            shiwake.owner = self.request.user
            shiwake.created_at = timezone.now()
            shiwake.updated_at = timezone.now()
            shiwake.shiwake_date = form.cleaned_data.get('shiwake_date')
            shiwake.save()

            # 借方
            for i in range(1, KANJO_ROWS + 1):
                if form.cleaned_data.get(f'kari_kanjo_kamoku_{i}') and form.cleaned_data.get(f'kari_amount_{i}'):
                    kanjo = Kanjo()
                    kanjo.shiwake = shiwake
                    kanjo.taishaku = True
                    kanjo.kanjo_kamoku = form.cleaned_data.get(f'kari_kanjo_kamoku_{i}')
                    kanjo.amount = form.cleaned_data.get(f'kari_amount_{i}')
                    kanjo.save()
            
            # 貸方
            for i in range(1, KANJO_ROWS + 1):
                if form.cleaned_data.get(f'kashi_kanjo_kamoku_{i}') and form.cleaned_data.get(f'kashi_amount_{i}'):
                    kanjo = Kanjo()
                    kanjo.shiwake = shiwake
                    kanjo.taishaku = False
                    kanjo.kanjo_kamoku = form.cleaned_data.get(f'kashi_kanjo_kamoku_{i}')
                    kanjo.amount = form.cleaned_data.get(f'kashi_amount_{i}')
                    kanjo.save()

        return HttpResponseRedirect(self.success_url)

#class Child2Inline(InlineFormSetFactory):
#    model = Kanjo
#    fields = '__all__'
#    factory_kwargs = {'extra': 5,'can_order': False, 'can_delete': False}

class ShiwakeCreateView(CustomLoginRequiredMixin, CreateView):
    """
    ビュー：登録画面
    """
    model = Shiwake
    form_class = ShiwakeForm_temp2
    success_url = reverse_lazy('shiwake_list')

    
    """def form_valid(self, form):
        logger.info("saving")
        shiwake = form.save(commit=False)
        shiwake.owner = self.request.user
        shiwake.created_at = timezone.now()
        shiwake.updated_at = timezone.now()
        shiwake.save()

        return HttpResponseRedirect(self.success_url)"""
    
