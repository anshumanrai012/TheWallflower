# Generated by Django 2.1.5 on 2020-05-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_auto_20200509_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='display_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='post',
            name='image_caption',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]