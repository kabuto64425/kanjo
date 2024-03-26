from django.urls import path

from .views import ShiwakeListView, ShiwakeCreateView, TestFormView

# アプリケーションのルーティング設定

urlpatterns = [
    path('list', ShiwakeListView.as_view(), name='shiwake_list'),
    path('create/', TestFormView.as_view(), name='shiwake_create'),
]
