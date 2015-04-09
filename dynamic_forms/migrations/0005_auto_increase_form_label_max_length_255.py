# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_forms', '0004_formmodel_recipient_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfieldmodel',
            name='label',
            field=models.CharField(max_length=255, verbose_name='Label'),
            preserve_default=True,
        ),
    ]
