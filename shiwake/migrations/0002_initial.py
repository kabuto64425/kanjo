# Generated by Django 3.2.23 on 2024-03-27 06:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shiwake', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='shiwake',
            name='owner',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shiwake_owner', to=settings.AUTH_USER_MODEL, verbose_name='所有者'),
        ),
        migrations.AddField(
            model_name='kanjo',
            name='shiwake',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='kanjos', to='shiwake.shiwake', verbose_name='仕訳'),
        ),
    ]
