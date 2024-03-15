from django.urls import path

from .views import DeckListView, DeckCreateView, DeckUpdateView, DeckDeleteView

# アプリケーションのルーティング設定

urlpatterns = [
    path('list', DeckListView.as_view(), name='deck_list'),
    path('create/', DeckCreateView.as_view(), name='deck_create'),
    path('update/<int:pk>/', DeckUpdateView.as_view(), name='deck_update'),
    path('delete/<int:pk>/', DeckDeleteView.as_view(), name='deck_delete'),
]
