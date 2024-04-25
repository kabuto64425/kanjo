from django.urls import path

from .views import KanjoMotochoView

# アプリケーションのルーティング設定
urlpatterns = [
    path('kanjo_motocho', KanjoMotochoView.as_view(), name='kanjo_motocho')
]
