# Generated by Django 2.1.5 on 2020-04-15 15:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20200415_2036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 15, 34, 59, 532409, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='author',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 15, 34, 59, 532409, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 15, 34, 59, 530410, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='postcomment',
            name='comment_at',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 21, 4, 59, 534409)),
        ),
    ]