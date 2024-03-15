from django.db import models

from users.models import User

class Deck(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # デッキ名
    deck_name = models.CharField(
        verbose_name='デッキ名',
        max_length=20,
        blank=False,
        null=False,
    )

    # デッキ名
    public_flag = models.BooleanField(
        verbose_name='全体公開',
        default=False,
        blank=False,
        null=False,
    )

    # 以下、管理項目

    # 所有者(ユーザー)
    owner = models.ForeignKey(
        User,
        verbose_name='所有者',
        blank=True,
        null=True,
        related_name='deck_owner',
        on_delete=models.SET_NULL,
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

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.deck_name

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'デッキ'
        verbose_name_plural = 'デッキ'
