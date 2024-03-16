from django.db import models
from users.models import User

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
        blank=True,
        null=True,
    )

    # 以下、管理項目

    # 所有者(ユーザー)
    owner = models.ForeignKey(
        User,
        verbose_name='所有者',
        blank=True,
        null=True,
        related_name='shiwake_owner',
        on_delete=models.CASCADE,
        editable=False,
    )

    # 作成時間
    created_at = models.DateTimeField(
        verbose_name='作成時間',
        blank=True,
        null=True,
        editable=False,
    )

    # 更新時間
    updated_at = models.DateTimeField(
        verbose_name='更新時間',
        blank=True,
        null=True,
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

    kanjo_kamoku = models.CharField(
        verbose_name='勘定科目',
        max_length=20,
        blank=False,
        null=False,
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
        related_name='kanjos',
        on_delete=models.CASCADE,
        #editable=False,
    )

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '勘定'
        verbose_name_plural = '勘定'
