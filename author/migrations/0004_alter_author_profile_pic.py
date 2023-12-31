# Generated by Django 4.2.1 on 2023-06-06 05:21

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_remove_author_email_remove_author_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default=None, force_format=None, keep_meta=True, null=True, quality=100, scale=None, size=[50, 80], upload_to='profile_pics/'),
        ),
    ]
