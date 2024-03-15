from django.urls import path

from .views import TopView, AskQuestionView, BottomView

# アプリケーションのルーティング設定

urlpatterns = [
    path('deck_<int:deck_pk>/top', TopView.as_view(), name='ask_question_top'),
    path('deck_<int:deck_pk>/<int:number>', AskQuestionView.as_view(), name='ask_question'),
    path('deck_<int:deck_pk>/bottom', BottomView.as_view(), name='ask_question_bottom')
]
