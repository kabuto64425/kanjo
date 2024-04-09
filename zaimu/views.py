from django.shortcuts import render
from django.views.generic import TemplateView
from utils.mixins import CustomLoginRequiredMixin
from shiwake.models import Shiwake, Kanjo
# Create your views here.

class TaishakuSonekiView(CustomLoginRequiredMixin, TemplateView):
    template_name = "zaimu/taishaku_soneki.html"

    def get_context_data(self, **kwargs):
        Kanjo.objects.select_related('shiwake').select_related('kanjo_kamoku')