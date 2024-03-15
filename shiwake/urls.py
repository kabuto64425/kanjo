from django.urls import path

from .views import ShiwakeListView

# アプリケーションのルーティング設定

urlpatterns = [
    path('list', ShiwakeListView.as_view(), name='shiwake_list'),
]
