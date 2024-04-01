from django.contrib import admin
from django.utils import timezone

from .models import Shiwake, Kanjo

@admin.register(Shiwake)
class ShiwakeAdmin(admin.ModelAdmin):
    readonly_fields = ('owner', 'id')
        
    def save_model(self, request, obj, form, change):
        # update_dateを現在時刻に更新
        obj.owner = request.user
        obj.created_at = timezone.now()
        obj.updated_at = timezone.now()
        # save_model関数をオーバーライドしてデータベースに変更を反映
        super(ShiwakeAdmin, self).save_model(request, obj, form, change)
    
    """
    管理画面上の動作の設定
      項目の表示非表示や検索項目の指定が可能
    参考：
    ・公式 The Django admin site
    https://docs.djangoproject.com/ja/2.1/ref/contrib/admin/
    ・Django 管理画面逆引きメモ
    https://qiita.com/zenwerk/items/044c149d93db097cdaf8
    ・ModelAdminをカスタマイズする方法
    https://qiita.com/cnloni/items/9d3ed9394c2ad935d1f7#modeladmin%E3%82%92%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%9E%E3%82%A4%E3%82%BA%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95
    """
    class Meta:
        pass

@admin.register(Kanjo)
class KanjoAdmin(admin.ModelAdmin):
    readonly_fields = ()
    
    """
    管理画面上の動作の設定
      項目の表示非表示や検索項目の指定が可能
    参考：
    ・公式 The Django admin site
    https://docs.djangoproject.com/ja/2.1/ref/contrib/admin/
    ・Django 管理画面逆引きメモ
    https://qiita.com/zenwerk/items/044c149d93db097cdaf8
    ・ModelAdminをカスタマイズする方法
    https://qiita.com/cnloni/items/9d3ed9394c2ad935d1f7#modeladmin%E3%82%92%E3%82%AB%E3%82%B9%E3%82%BF%E3%83%9E%E3%82%A4%E3%82%BA%E3%81%99%E3%82%8B%E6%96%B9%E6%B3%95
    """
    class Meta:
        pass

