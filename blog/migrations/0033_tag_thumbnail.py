# Generated by Django 2.1.5 on 2020-05-22 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0032_auto_20200521_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='thumbnail',
            field=models.ImageField(default='1.png', upload_to='media/tags'),
            preserve_default=False,
        ),
    ]