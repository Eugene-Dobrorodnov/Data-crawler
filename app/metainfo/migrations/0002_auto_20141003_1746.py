# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metainfo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='metainfo',
            name='domain',
            field=models.ForeignKey(to='metainfo.Domain', unique=True),
        ),
    ]
