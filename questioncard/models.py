from django.db import models

from deck.models import Deck

class QuestionCard(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # 問題文
    question_text = models.CharField(
        verbose_name='問題文',
        max_length=300,
        blank=False,
        null=False,
    )

    # 正解
    correct_answer = models.CharField(
        verbose_name='正解',
        max_length=300,
        blank=False,
        null=False,
    )

    # 出題順
    order = models.IntegerField(
        verbose_name='出題順',
        blank=False,
        null=False,
        #editable=False,
    )

    in_deck = models.ForeignKey(
        Deck,
        verbose_name='デッキ',
        blank=False,
        null=False,
        related_name='in_deck',
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

    def __str__(self):
        """
        リストボックスや管理画面での表示
        """
        return self.correct_answer

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = '問題カード'
        verbose_name_plural = '問題カード'
        constraints = [
            models.UniqueConstraint(fields=['in_deck', 'order'], name='unique__in_deck__order')
        ]
