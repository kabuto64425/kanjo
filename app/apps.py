from django.apps import AppConfig
from django.db.models.signals import post_migrate

class AppConfig(AppConfig):
    """
    アプリケーション構成クラス
    管理画面での表示名を指定する
    """
    name = 'app'
    verbose_name = '仕訳登録アプリ'

    def ready(self):
        from .models import create_default_group
        post_migrate.connect(create_default_group, sender=self)
