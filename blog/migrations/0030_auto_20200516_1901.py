# Generated by Django 2.1.5 on 2020-05-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0029_auto_20200515_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='picture',
            field=models.ImageField(default='media/profile.png', upload_to='media/profiles'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='display_image',
            field=models.ImageField(upload_to='media'),
        ),
    ]
