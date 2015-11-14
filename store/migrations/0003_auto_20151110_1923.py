# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20151110_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(unique=True, max_length=320),
        ),
    ]
