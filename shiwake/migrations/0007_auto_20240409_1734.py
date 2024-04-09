# Generated by Django 3.2.23 on 2024-04-09 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shiwake', '0006_auto_20240328_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kanjo',
            name='kanjo_kamoku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='master_kanjo_kamoku_kanjos', to='app.masterkanjokamoku', verbose_name='勘定科目'),
        ),
        migrations.AlterField(
            model_name='kanjo',
            name='shiwake',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shiwake_kanjos', to='shiwake.shiwake', verbose_name='仕訳'),
        ),
        migrations.AlterField(
            model_name='shiwake',
            name='owner',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='user_shiwakes', to=settings.AUTH_USER_MODEL, verbose_name='所有者'),
        ),
    ]
