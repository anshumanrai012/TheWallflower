# Generated by Django 2.1.5 on 2020-05-15 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0028_auto_20200515_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='display_image',
            field=models.ImageField(default='1.png', upload_to='media/'),
            preserve_default=False,
        ),
    ]
