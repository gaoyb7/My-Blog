# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_post_visited'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='has_read',
            field=models.BooleanField(default=False),
        ),
    ]
