# Generated by Django 3.2.19 on 2023-06-20 10:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deck_name', models.CharField(blank=True, max_length=20, null=True, verbose_name='デッキ名')),
                ('created_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='作成時間')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='更新時間')),
                ('owner', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='deck_owner', to=settings.AUTH_USER_MODEL, verbose_name='所有者')),
            ],
            options={
                'verbose_name': 'デッキ',
                'verbose_name_plural': 'デッキ',
            },
        ),
    ]
