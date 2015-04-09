# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_forms', '0002_auto_20140124_1844'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formfieldmodel',
            name='parent_form',
            field=models.ForeignKey(related_name='fields', to='dynamic_forms.FormModel'),
        ),
        migrations.AlterField(
            model_name='formmodeldata',
            name='form',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='data', to='dynamic_forms.FormModel'),
        ),
    ]
