from django.urls import path

from .views import TaishakuSonekiView

# アプリケーションのルーティング設定
urlpatterns = [
    path('taishaku_soneki', TaishakuSonekiView.as_view(), name='taishaku_soneki')
]
