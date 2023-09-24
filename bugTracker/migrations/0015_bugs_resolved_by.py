# Generated by Django 4.2.4 on 2023-09-16 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bugTracker', '0014_alter_bugs_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='bugs',
            name='resolved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='resolved_bugs', to=settings.AUTH_USER_MODEL),
        ),
    ]