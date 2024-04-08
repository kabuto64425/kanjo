from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core import validators

class User(AbstractUser):
    """
    カスタムユーザー データ定義クラス

    ユーザーの管理項目を増やしたい場合はここにフィールドを定義します。
    例：住所、電話番号など
    """
    nick_name = models.CharField(
        verbose_name='ニックネーム',
        max_length=150,
        blank=False,
        null=True
    )

    last_month = models.IntegerField(
        verbose_name='決算月',
        default=3,
        blank=False,
        null=False,
        validators=[validators.MinValueValidator(1),
                    validators.MaxValueValidator(12)]
    )

    last_day = models.IntegerField(
        verbose_name='決算日',
        default=31,
        blank=False,
        null=False,
        validators=[validators.MinValueValidator(1),
                    validators.MaxValueValidator(31)]
    )

    uuid_for_google_form = models.CharField(
        verbose_name='googleフォームに送信するためのuuid',
        max_length=40,
        blank=True,
        null=True,
        editable=False,
    )

    #objects = UserManager()
