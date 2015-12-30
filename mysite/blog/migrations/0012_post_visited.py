# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_auto_20151229_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='visited',
            field=models.IntegerField(default=0),
        ),
    ]
