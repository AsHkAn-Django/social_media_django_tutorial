# Generated by Django 5.2.1 on 2025-05-18 08:15

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0004_comment_like'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-like']},
        ),
        migrations.RemoveIndex(
            model_name='comment',
            name='myApp_comme_created_1dd776_idx',
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['-like'], name='myApp_comme_like_aeae81_idx'),
        ),
    ]
