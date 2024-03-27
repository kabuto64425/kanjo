# Generated by Django 3.2.23 on 2024-03-27 07:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shiwake', '0004_alter_shiwake_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shiwake',
            name='owner',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shiwake_owner', to=settings.AUTH_USER_MODEL, verbose_name='所有者'),
        ),
    ]