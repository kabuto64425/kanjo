from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.edit import FormView, DeleteView
from django.db import transaction
from django.db.models import Avg,Sum,Max,Min,Count
from utils.mixins import CustomLoginRequiredMixin
from django.core.exceptions import PermissionDenied

from django.views.generic import ListView
from .models import Shiwake, Kanjo
from .forms import ShiwakeForm
from config.consts import KANJO_ROWS
from utils import common
from datetime import datetime, date, time
from dateutil import relativedelta

import logging

logger = logging.getLogger(__name__)

class ShiwakeEntity:
    def __init__(self, shiwake):
        self.id = shiwake.id
        self.shiwake_date = shiwake.shiwake_date

        kanjo_list = shiwake.kanjos.all()
        self.kari_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == True]
        self.kashi_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == False]

        self.kari_amount_sum = sum([kanjo.amount for kanjo in self.kari_kanjo_list])
        self.kashi_amount_sum = sum([kanjo.amount for kanjo in self.kashi_kanjo_list])

# Create your views here.
class ShiwakeListView(CustomLoginRequiredMixin, ListView):

    def get(self, request, **kwargs):
        """
        リクエスト受付
        セッション変数の管理:一覧画面と詳細画面間の移動時に検索条件が維持されるようにする。
        """
        return super().get(request, **kwargs)
    
    def find_period_from_queryparam(self):
        query_last_day = self.request.GET.get('last_day')

        if query_last_day:
            target = timezone.make_aware(datetime.strptime(query_last_day, '%Y-%m-%d'))
            return common.find_peripd(target, 3, 31)
        else:
            return common.find_peripd(timezone.now(), 3, 31)

    def get_queryset(self):
        """
        ソート順・デフォルトの絞り込みを指定
        """
        user = self.request.user  # ログインユーザーモデルの取得

        period = self.find_period_from_queryparam()

        first_datetime = period[0]
        last_datetime = period[1]

        filters = {
            "owner" : user,
            "shiwake_date__gte": first_datetime,
            "shiwake_date__lte": last_datetime,
        }

        return Shiwake.objects.prefetch_related('kanjos').filter(**filters).order_by('shiwake_date')
    
    def get_context_data(self, *, object_list=None, **kwargs):
        """
        表示データの設定
        """
        # 表示データを追加したい場合は、ここでキーを追加しテンプレート上で表示する
        # 例：kwargs['sample'] = 'sample'
        context = super().get_context_data(object_list=object_list, **kwargs)

        period_from_queryparam = self.find_period_from_queryparam()

        context['selected'] = period_from_queryparam[1]

        user = self.request.user  # ログインユーザーモデルの取得

        aggreate_shiwake_date__max = Shiwake.objects.all().filter(owner=user).aggregate(Max("shiwake_date"))
        aggreate_shiwake_date__min = Shiwake.objects.all().filter(owner=user).aggregate(Min("shiwake_date"))
        
        shiwake_date__max = aggreate_shiwake_date__max["shiwake_date__max"]
        shiwake_date__min = aggreate_shiwake_date__min["shiwake_date__min"]

        candidate_dates = [timezone.make_aware(datetime.combine(date, time())) for date in [shiwake_date__max, shiwake_date__min, timezone.now().date()]]

        periods = [common.find_peripd(candidate_date, 3, 31) for candidate_date in candidate_dates]

        last_day_of_earliest = min(periods)[1]
        last_day_of_latest = max(periods)[1]

        select_options = []

        for current_year in range(last_day_of_earliest.year, last_day_of_latest.year + 1):
            select_options.append(common.find_period_from_year(current_year, 3, 31))

        context['select_option_list'] = select_options

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
    
class ShiwakeUpdateView(CustomLoginRequiredMixin, FormView):
    # テンプレート名の設定
    template_name = 'shiwake/shiwake_form.html'

    # フォームの設定
    form_class = ShiwakeForm
    success_url = reverse_lazy('shiwake_list')

    def get_object(self, queryset=None):
        shiwake = Shiwake.objects.prefetch_related('kanjos').get(pk=self.kwargs['pk'])
         # 自身の仕訳に対してほかユーザーがアクセスするのを防ぐため
        if self.request.user == shiwake.owner:
            return shiwake
        else:
            raise PermissionDenied
    
    def get_initial(self):
        shiwake = self.get_object()
        res = {'shiwake_date': shiwake.shiwake_date}

        kanjo_list = shiwake.kanjos.all()
        kari_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == True]
        for i, kari_kanjo in enumerate(kari_kanjo_list, 1):
            res[f'kari_kanjo_kamoku_{i}'] = kari_kanjo.kanjo_kamoku
            res[f'kari_amount_{i}'] = kari_kanjo.amount

        kashi_kanjo_list = [kanjo for kanjo in kanjo_list if kanjo.taishaku == False]
        for i, kashi_kanjo in enumerate(kashi_kanjo_list, 1):
            res[f'kashi_kanjo_kamoku_{i}'] = kashi_kanjo.kanjo_kamoku
            res[f'kashi_amount_{i}'] = kashi_kanjo.amount

        return res
    
    def form_valid(self, form):
        with transaction.atomic():
            shiwake = self.get_object()
            shiwake.owner = self.request.user
            shiwake.updated_at = timezone.now()
            shiwake.shiwake_date = form.cleaned_data.get('shiwake_date')
            shiwake.save()

            shiwake.kanjos.all().delete()

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