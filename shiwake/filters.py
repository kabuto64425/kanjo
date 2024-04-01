import django_filters
from django.db import models

from .models import Shiwake


class OrderingFilter(django_filters.filters.OrderingFilter):
    """日本語対応"""
    descending_fmt = '%s （降順）'


class ShiwakeFilterSet(django_filters.FilterSet):
    """
     django-filter 構成クラス
    https://django-filter.readthedocs.io/en/latest/ref/filterset.html
    """
    #shiwake_date = django_filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Shiwake
        # 一部フィールドを除きモデルクラスの定義を全て引用する
        fields  = ['shiwake_date']
