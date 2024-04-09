from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class TaishakuSonekiView(TemplateView):
    template_name = "zaimu/taishaku_soneki.html"