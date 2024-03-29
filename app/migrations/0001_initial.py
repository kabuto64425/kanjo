# Generated by Django 3.2.23 on 2024-03-27 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sample_1', models.CharField(blank=True, max_length=20, null=True, verbose_name='サンプル項目1 文字列')),
                ('sample_2', models.TextField(blank=True, null=True, verbose_name='サンプル項目2 メモ')),
                ('sample_3', models.IntegerField(blank=True, null=True, verbose_name='サンプル項目3 整数')),
                ('sample_4', models.FloatField(blank=True, null=True, verbose_name='サンプル項目4 浮動小数点')),
                ('sample_5', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='サンプル項目5 固定小数点')),
                ('sample_6', models.BooleanField(verbose_name='サンプル項目6 ブール値')),
                ('sample_7', models.DateField(blank=True, null=True, verbose_name='サンプル項目7 日付')),
                ('sample_8', models.DateTimeField(blank=True, null=True, verbose_name='サンプル項目8 日時')),
                ('sample_9', models.IntegerField(blank=True, choices=[(1, '選択１'), (2, '選択２'), (3, '選択３')], null=True, verbose_name='サンプル項目9_選択肢（固定）')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='作成時間')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='更新時間')),
            ],
            options={
                'verbose_name': 'サンプル',
                'verbose_name_plural': 'サンプル',
            },
        ),
        migrations.CreateModel(
            name='MasterKanjoKamoku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='勘定科目名')),
                ('kamoku_type', models.IntegerField(choices=[(1, '資産'), (2, '負債'), (3, '純資産'), (4, '費用'), (5, '収益')])),
            ],
        ),
    ]
