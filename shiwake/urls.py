from django.urls import path

from .views import ShiwakeListView, ShiwakeCreateView

# アプリケーションのルーティング設定

urlpatterns = [
    path('list', ShiwakeListView.as_view(), name='shiwake_list'),
    path('create/', ShiwakeCreateView.as_view(), name='shiwake_create'),
]
