from django.urls import path

from .views import QuestionCardListView, QuestionCardCreateView, QuestionCardUpdateView, QuestionCardDeleteView, QuestionCardSwapOrderApiView

# アプリケーションのルーティング設定

urlpatterns = [
    path('list/deck_<int:deck_pk>/', QuestionCardListView.as_view(), name='question_card_list'),
    path('create/deck_<int:deck_pk>/', QuestionCardCreateView.as_view(), name='question_card_create'),
    path('update/<int:pk>/', QuestionCardUpdateView.as_view(), name='question_card_update'),
    path('delete/<int:pk>/', QuestionCardDeleteView.as_view(), name='question_card_delete'),
    path('swap', QuestionCardSwapOrderApiView.as_view(), name='question_card_swap'),
]
