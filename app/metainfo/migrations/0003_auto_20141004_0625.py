# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metainfo', '0002_auto_20141003_1746'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='metainfo',
            name='favicon',
        ),
        migrations.AddField(
            model_name='metainfo',
            name='image',
            field=models.URLField(null=True, verbose_name=b'image', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='metainfo',
            name='title',
            field=models.TextField(null=True, verbose_name='title', blank=True),
            preserve_default=True,
        ),
    ]
