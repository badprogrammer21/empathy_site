# Generated by Django 4.2.1 on 2023-06-06 03:24

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='photo',
        ),
        migrations.AddField(
            model_name='author',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default=None, force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[50, 80], upload_to='authors'),
        ),
    ]