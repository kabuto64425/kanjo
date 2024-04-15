from django.db import models

from users.models import User

class MasterKanjoKamokuType(models.IntegerChoices):
    SHISAN = 1, '資産'
    FUSAI = 2, '負債'
    JUNSHISAN = 3, '純資産'
    HIYO = 4, '費用'
    SHUEKI = 5, '収益'

class MasterKanjoKamoku(models.Model):
    name = models.CharField(
        verbose_name='勘定科目名',
        max_length=50,
        unique=True,
        blank=False,
        null=False,
    )

    kamoku_type = models.IntegerField(
        blank=False,
        null=False,
        choices=MasterKanjoKamokuType.choices
    )

    def __str__(self):
        return self.name

def create_default_group(sender, **kwargs):
    MasterKanjoKamoku.objects.get_or_create(name='現金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='小口現金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='当座預金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='普通預金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='定期預金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='受取手形', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='売掛金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='クレジット売掛金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='電子記録債権', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='繰越商品', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='貸付金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='手形貸付金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='役員貸付金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='従業員貸付金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='前払金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='未収入金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='仮払金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='受取商品券', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='差入保証金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='貯蔵品', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='仮払消費税', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='未収還付消費税', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='仮払法人税等', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='前払費用', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='未収収益', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='建物', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='備品', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='車両運搬具', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='土地', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='建物減価償却累計額', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='備品減価償却累計額', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='車両運搬具減価償却累計額', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='貸倒引当金', kamoku_type=MasterKanjoKamokuType.SHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='現金過不足', kamoku_type=MasterKanjoKamokuType.SHISAN)

    MasterKanjoKamoku.objects.get_or_create(name='支払手形', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='買掛金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='電子記録債務', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='前受金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='借入金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='役員借入金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='手形借入金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='当座借越', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='未払金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='仮受金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='未払費用', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='前受収益', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='預り金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='所得税預り金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='社会保険料預り金', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='仮受消費税', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='未払消費税', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='未払法人税等', kamoku_type=MasterKanjoKamokuType.FUSAI)
    MasterKanjoKamoku.objects.get_or_create(name='未払配当金', kamoku_type=MasterKanjoKamokuType.FUSAI)

    MasterKanjoKamoku.objects.get_or_create(name='資本金', kamoku_type=MasterKanjoKamokuType.JUNSHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='利益準備金', kamoku_type=MasterKanjoKamokuType.JUNSHISAN)
    MasterKanjoKamoku.objects.get_or_create(name='繰越利益剰余金', kamoku_type=MasterKanjoKamokuType.JUNSHISAN)

    MasterKanjoKamoku.objects.get_or_create(name='仕入', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='売上原価', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='発送費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='給料', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='法定福利費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='広告宣伝費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='支払手数料', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='支払利息', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='旅費交通費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='貸倒引当金繰入', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='貸倒損失', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='減価償却費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='通信費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='消耗品費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='水道光熱費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='支払家賃', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='支払地代', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='保険料', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='租税公課', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='修繕費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='雑費', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='雑損', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='固定資産売却損', kamoku_type=MasterKanjoKamokuType.HIYO)
    MasterKanjoKamoku.objects.get_or_create(name='法人税等', kamoku_type=MasterKanjoKamokuType.HIYO)

    MasterKanjoKamoku.objects.get_or_create(name='売上', kamoku_type=MasterKanjoKamokuType.SHUEKI)
    MasterKanjoKamoku.objects.get_or_create(name='受取家賃', kamoku_type=MasterKanjoKamokuType.SHUEKI)
    MasterKanjoKamoku.objects.get_or_create(name='受取地代', kamoku_type=MasterKanjoKamokuType.SHUEKI)
    MasterKanjoKamoku.objects.get_or_create(name='受取手数料', kamoku_type=MasterKanjoKamokuType.SHUEKI)
    MasterKanjoKamoku.objects.get_or_create(name='受取利息', kamoku_type=MasterKanjoKamokuType.SHUEKI)
    MasterKanjoKamoku.objects.get_or_create(name='雑益', kamoku_type=MasterKanjoKamokuType.SHUEKI)
    MasterKanjoKamoku.objects.get_or_create(name='貸倒引当金戻入', kamoku_type=MasterKanjoKamokuType.SHUEKI)
    MasterKanjoKamoku.objects.get_or_create(name='償却債権取立益', kamoku_type=MasterKanjoKamokuType.SHUEKI)
    MasterKanjoKamoku.objects.get_or_create(name='固定資産売却益', kamoku_type=MasterKanjoKamokuType.SHUEKI)

class Item(models.Model):
    """
    データ定義クラス
      各フィールドを定義する
    参考：
    ・公式 モデルフィールドリファレンス
    https://docs.djangoproject.com/ja/2.1/ref/models/fields/
    """

    # サンプル項目1 文字列
    sample_1 = models.CharField(
        verbose_name='サンプル項目1 文字列',
        max_length=20,
        blank=True,
        null=True,
    )

    # サンプル項目2 メモ
    sample_2 = models.TextField(
        verbose_name='サンプル項目2 メモ',
        blank=True,
        null=True,
    )

    # サンプル項目3 整数
    sample_3 = models.IntegerField(
        verbose_name='サンプル項目3 整数',
        blank=True,
        null=True,
    )

    # サンプル項目4 浮動小数点
    sample_4 = models.FloatField(
        verbose_name='サンプル項目4 浮動小数点',
        blank=True,
        null=True,
    )

    # サンプル項目5 固定小数点
    sample_5 = models.DecimalField(
        verbose_name='サンプル項目5 固定小数点',
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
    )

    # サンプル項目6 ブール値
    sample_6 = models.BooleanField(
        verbose_name='サンプル項目6 ブール値',
    )

    # サンプル項目7 日付
    sample_7 = models.DateField(
        verbose_name='サンプル項目7 日付',
        blank=True,
        null=True,
    )

    # サンプル項目8 日時
    sample_8 = models.DateTimeField(
        verbose_name='サンプル項目8 日時',
        blank=True,
        null=True,
    )

    # サンプル項目9 選択肢（固定）
    sample_9_choice = (
        (1, '選択１'),
        (2, '選択２'),
        (3, '選択３'),
    )

    sample_9 = models.IntegerField(
        verbose_name='サンプル項目9_選択肢（固定）',
        choices=sample_9_choice,
        blank=True,
        null=True,
    )

    # サンプル項目9 選択肢（マスタ連動）
    sample_10 = models.ForeignKey(
        User,
        verbose_name='サンプル項目10_選択肢（マスタ連動）',
        blank=True,
        null=True,
        related_name='sample_10',
        on_delete=models.SET_NULL,
    )

    # 以下、管理項目

    # 作成者(ユーザー)
    created_by = models.ForeignKey(
        User,
        verbose_name='作成者',
        blank=True,
        null=True,
        related_name='CreatedBy',
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

    # 更新者(ユーザー)
    updated_by = models.ForeignKey(
        User,
        verbose_name='更新者',
        blank=True,
        null=True,
        related_name='UpdatedBy',
        on_delete=models.SET_NULL,
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
        return self.sample_1

    class Meta:
        """
        管理画面でのタイトル表示
        """
        verbose_name = 'サンプル'
        verbose_name_plural = 'サンプル'
