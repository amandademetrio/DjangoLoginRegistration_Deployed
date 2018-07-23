# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-23 18:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0003_quote_quote'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('liked_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='first_app.Quote')),
                ('liker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_messages', to='first_app.User')),
            ],
        ),
    ]