from django.urls import path

from .views import IndexView, VueTestView

# アプリケーションのルーティング設定

urlpatterns = [
    path('top', IndexView.as_view(), name='top'),
    path('vuetest', VueTestView.as_view(), name='vuetest')
]
