from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import FormView, DeleteView
from django.db import transaction
from django.db.models import Max,Min
from utils.mixins import CustomLoginRequiredMixin, AccountingPeriodLoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Prefetch

from django.views.generic import ListView
from .models import Shiwake, Kanjo
from .forms import ShiwakeForm
from app.models import MasterKanjoKamoku
from config.consts import KANJO_ROWS

import logging

logger = logging.getLogger(__name__)

class ShiwakeEntity:
    def __init__(self, shiwake):
        self.id = shiwake.id
        self.shiwake_date = shiwake.shiwake_date

        kanjo_list = shiwake.shiwake_kanjos.all()
        self.kari_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == True]
        self.kashi_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == False]

        self.kari_amount_sum = sum([kanjo.amount for kanjo in self.kari_kanjo_list])
        self.kashi_amount_sum = sum([kanjo.amount for kanjo in self.kashi_kanjo_list])

# Create your views here.
class ShiwakeListView(AccountingPeriodLoginRequiredMixin, ListView):

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

        period = self.find_period_from_queryparam("last_day")

        filters = {
            "owner" : user,
            "shiwake_date__gte": period[0],
            "shiwake_date__lte": period[1],
        }

        return Shiwake.objects.prefetch_related(Prefetch('shiwake_kanjos',queryset=Kanjo.objects.select_related('kanjo_kamoku'))).filter(**filters).order_by('shiwake_date')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)

        period_from_queryparam = self.find_period_from_queryparam("last_day")

        context['selected'] = period_from_queryparam[1]

        context['select_option_list'] = self.create_period_selector_choices()

        context['shiwake_entity_list'] = [ShiwakeEntity(shiwake) for shiwake in context['shiwake_list']]
        return context

class ShiwakeCreateView(CustomLoginRequiredMixin, FormView):
    # テンプレート名の設定
    template_name = 'shiwake/shiwake_form.html'
    # フォームの設定
    form_class = ShiwakeForm
    success_url = reverse_lazy('shiwake_list')
    def form_valid(self, form):
        with transaction.atomic():
            shiwake = Shiwake()
            shiwake.owner = self.request.user
            shiwake.created_at = timezone.now()
            shiwake.updated_at = timezone.now()
            shiwake.shiwake_date = form.cleaned_data.get('shiwake_date')
            shiwake.save()

            kanjos = []

            # 借方
            for i in range(1, KANJO_ROWS + 1):
                if form.cleaned_data.get(f'kari_kanjo_kamoku_{i}') and form.cleaned_data.get(f'kari_amount_{i}'):
                    kanjo = Kanjo()
                    kanjo.shiwake = shiwake
                    kanjo.taishaku = True
                    kanjo.kanjo_kamoku = MasterKanjoKamoku.objects.get(id=form.cleaned_data.get(f'kari_kanjo_kamoku_{i}'))
                    kanjo.amount = form.cleaned_data.get(f'kari_amount_{i}')
                    kanjos.append(kanjo)

            # 貸方
            for i in range(1, KANJO_ROWS + 1):
                if form.cleaned_data.get(f'kashi_kanjo_kamoku_{i}') and form.cleaned_data.get(f'kashi_amount_{i}'):
                    kanjo = Kanjo()
                    kanjo.shiwake = shiwake
                    kanjo.taishaku = False
                    kanjo.kanjo_kamoku = MasterKanjoKamoku.objects.get(id=form.cleaned_data.get(f'kashi_kanjo_kamoku_{i}'))
                    kanjo.amount = form.cleaned_data.get(f'kashi_amount_{i}')
                    kanjos.append(kanjo)

            Kanjo.objects.bulk_create(kanjos)

        return HttpResponseRedirect(self.success_url)
    
class ShiwakeUpdateView(CustomLoginRequiredMixin, FormView):
    # テンプレート名の設定
    template_name = 'shiwake/shiwake_form.html'

    # フォームの設定
    form_class = ShiwakeForm
    success_url = reverse_lazy('shiwake_list')

    def get_object(self, queryset=None):
        shiwake = Shiwake.objects.prefetch_related(Prefetch('shiwake_kanjos',queryset=Kanjo.objects.select_related('kanjo_kamoku'))).get(pk=self.kwargs['pk'])
         # 自身の仕訳に対してほかユーザーがアクセスするのを防ぐため
        if self.request.user == shiwake.owner:
            return shiwake
        else:
            raise PermissionDenied
    
    def get_initial(self):
        shiwake = self.get_object()
        res = {'shiwake_date': shiwake.shiwake_date}

        kanjo_list = shiwake.shiwake_kanjos.all()
        kari_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == True]
        for i, kari_kanjo in enumerate(kari_kanjo_list, 1):
            res[f'kari_kanjo_kamoku_{i}'] = kari_kanjo.kanjo_kamoku.id
            res[f'kari_amount_{i}'] = kari_kanjo.amount

        kashi_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == False]
        for i, kashi_kanjo in enumerate(kashi_kanjo_list, 1):
            res[f'kashi_kanjo_kamoku_{i}'] = kashi_kanjo.kanjo_kamoku.id
            res[f'kashi_amount_{i}'] = kashi_kanjo.amount

        return res
    
    def form_valid(self, form):
        with transaction.atomic():
            shiwake = self.get_object()
            shiwake.owner = self.request.user
            shiwake.updated_at = timezone.now()
            shiwake.shiwake_date = form.cleaned_data.get('shiwake_date')
            shiwake.save()

            shiwake.shiwake_kanjos.all().delete()

            kanjos = []

            # 借方
            for i in range(1, KANJO_ROWS + 1):
                if form.cleaned_data.get(f'kari_kanjo_kamoku_{i}') and form.cleaned_data.get(f'kari_amount_{i}'):
                    kanjo = Kanjo()
                    kanjo.shiwake = shiwake
                    kanjo.taishaku = True
                    kanjo.kanjo_kamoku = MasterKanjoKamoku.objects.get(id=form.cleaned_data.get(f'kari_kanjo_kamoku_{i}'))
                    kanjo.amount = form.cleaned_data.get(f'kari_amount_{i}')
                    kanjos.append(kanjo)

            # 貸方
            for i in range(1, KANJO_ROWS + 1):
                if form.cleaned_data.get(f'kashi_kanjo_kamoku_{i}') and form.cleaned_data.get(f'kashi_amount_{i}'):
                    kanjo = Kanjo()
                    kanjo.shiwake = shiwake
                    kanjo.taishaku = False
                    kanjo.kanjo_kamoku = MasterKanjoKamoku.objects.get(id=form.cleaned_data.get(f'kashi_kanjo_kamoku_{i}'))
                    kanjo.amount = form.cleaned_data.get(f'kashi_amount_{i}')
                    kanjos.append(kanjo)

            Kanjo.objects.bulk_create(kanjos)

        return HttpResponseRedirect(self.success_url)

class ShiwakeDeleteView(CustomLoginRequiredMixin, DeleteView):
    """
    ビュー：削除画面
    """
    model = Shiwake
    success_url = reverse_lazy('shiwake_list')

    # 自身のデッキに対してほかユーザーがアクセスするのを防ぐため
    def get(self, request, *args, **kwargs):
        shiwake = super().get_object()
        if self.request.user == shiwake.owner:
            return super().get(request, *args, **kwargs)
        else:
            raise PermissionDenied
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        context = super().get_context_data(object_list=object_list, **kwargs)

        context['shiwake_entity'] = ShiwakeEntity(super().get_object())
        return context