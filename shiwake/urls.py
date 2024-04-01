from django.urls import path

from .views import ShiwakeListView, ShiwakeCreateView, ShiwakeUpdateView, ShiwakeDeleteView

# アプリケーションのルーティング設定

urlpatterns = [
    path('list', ShiwakeListView.as_view(), name='shiwake_list'),
    path('create/', ShiwakeCreateView.as_view(), name='shiwake_create'),
    path('update/<int:pk>/', ShiwakeUpdateView.as_view(), name='shiwake_update'),
    path('delete/<int:pk>/', ShiwakeDeleteView.as_view(), name='shiwake_delete'),
]
