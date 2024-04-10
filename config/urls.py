"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf import settings

# ルーティング設定
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('shiwake/', include('shiwake.urls')),
    path('users/', include('users.urls')),
    path('', include('allauth.urls')),
    path('zaimu/', include('zaimu.urls')),
]

# 追加  '__debug__/'は他のURLに影響を及ぼさないならなんでも良い
if settings.DEBUG:
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]

# 管理サイトの見出しを変更可能
#  タイトル；タイトルタグで使用
admin.site.site_title = 'タイトル'
#  サイト名：ログイン画面と管理画面上部の表示
admin.site.site_header = '仕訳登録アプリ'
#  メニュー：管理画面の見出し表示
admin.site.index_title = 'メニュー'
