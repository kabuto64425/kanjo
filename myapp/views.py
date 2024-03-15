from django.shortcuts import render
#from django.contrib.auth.mixins import LoginRequiredMixin カスタムクラスを使用するため不要
from django.views.generic import TemplateView

from .mixins import CustomLoginRequiredMixin #追加

# このviewのルーティングは「/myapp/top」
class IndexView(CustomLoginRequiredMixin, TemplateView):
    template_name = "myapp/index.html"
    def get_context_data(self, **kwargs):
        kwargs["members"] = [
              { "name": "taro", "age": 25 },
              { "name": "jiro", "age": 26 },
              { "name": "hanako", "age": 29 },
              { "name": "emi", "age": 24 },
              { "name": "rin", "age": 22 },
              { "name": "koichi", "age": 30 },
        ]

        return super().get_context_data(**kwargs)

class VueTestView(TemplateView):
    template_name = "myapp/vuetest.html"
