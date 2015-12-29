# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20151225_2036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='tag_cn_name',
        ),
    ]
