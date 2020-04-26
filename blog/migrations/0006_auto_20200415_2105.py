# Generated by Django 2.1.5 on 2020-04-15 15:35

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200415_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 15, 35, 50, 797289, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='author',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 15, 35, 50, 798288, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 15, 35, 50, 795291, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='comment_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 15, 35, 50, 800289, tzinfo=utc)),
        ),
    ]
