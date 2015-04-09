# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_forms', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='formfieldmodel',
            unique_together=set([('parent_form', 'name')]),
        ),
        migrations.AddField(
            model_name='formmodeldata',
            name='display_key',
            field=models.CharField(max_length=24, help_text='A unique identifier that is used to allow users to view their sent data. Unique over all stored data sets.', blank=True, default=None, unique=True, verbose_name='Display key', null=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='formmodel',
            name='allow_display',
            field=models.BooleanField(default=False, verbose_name='Allow display', help_text='Allow a user to view the input at a later time. This requires the “Store in database” action to be active. The sender will be given a unique URL to recall the data.'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='formmodel',
            name='form_template',
            field=models.CharField(default='dynamic_forms/form.html', verbose_name='Form template path', choices=[
                ('dynamic_forms/form.html', 'Default form template')], max_length=100),
        ),
        migrations.AlterField(
            model_name='formmodel',
            name='success_template',
            field=models.CharField(default='dynamic_forms/form_success.html', verbose_name='Success template path', choices=[
                ('dynamic_forms/form_success.html', 'Default success template')], max_length=100),
        ),
    ]
