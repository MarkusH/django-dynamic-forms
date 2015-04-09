# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_forms', '0003_auto_20140916_1433'),
    ]

    operations = [
        migrations.AddField(
            model_name='formmodel',
            name='recipient_email',
            field=models.EmailField(help_text='Email address to send form data.', max_length=75, null=True, verbose_name='Recipient email', blank=True),
            preserve_default=True,
        ),
    ]
