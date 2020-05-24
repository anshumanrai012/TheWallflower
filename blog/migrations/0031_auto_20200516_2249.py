# Generated by Django 2.1.5 on 2020-05-16 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0030_auto_20200516_1901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='gender',
            field=models.CharField(choices=[('m', 'Male'), ('f', 'Female'), ('o', 'Others')], max_length=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='image_caption',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='post_content',
            field=models.TextField(max_length=100000),
        ),
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('d', 'Draft'), ('p', 'Published'), ('a', 'Archived')], default='p', max_length=1),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]