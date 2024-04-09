from django.db import models
from users.models import User
from app.models import MasterKanjoKamoku

# Create your models here.
class Shiwake(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # 日付
    shiwake_date = models.DateField(
        verbose_name='日付',
        blank=False,
        null=False,
    )

    # 以下、管理項目

    # 所有者(ユーザー)
    owner = models.ForeignKey(
        User,
        verbose_name='所有者',
        blank=False,
        null=False,
        related_name='user_shiwakes',
        on_delete=models.CASCADE,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=False,
        null=False,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=False,
        null=False,
        editable=False,
    )

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '仕訳'
        verbose_name_plural = '仕訳'

class Kanjo(models.Model):
    taishaku = models.BooleanField(
        verbose_name='貸借',
        default=True,
        blank=False,
        null=False,
        help_text='借方ならTrue'
    )

    kanjo_kamoku = models.ForeignKey(
        MasterKanjoKamoku,
        verbose_name='勘定科目',
        blank=False,
        null=False,
        related_name='master_kanjo_kamoku_kanjos',
        on_delete=models.PROTECT,
    )

    amount = models.IntegerField(
        verbose_name='金額',
        blank=False,
        null=False,
    )

    shiwake = models.ForeignKey(
        Shiwake,
        verbose_name='仕訳',
        blank=False,
        null=False,
        related_name='shiwake_kanjos',
        on_delete=models.CASCADE,
    )

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '勘定'
        verbose_name_plural = '勘定'
