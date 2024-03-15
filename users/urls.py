from django.urls import path

from .views import UserChangeView

# アプリケーションのルーティング設定
app_name = 'users'
urlpatterns = [
    path('update', UserChangeView.as_view(), name='update')
]
