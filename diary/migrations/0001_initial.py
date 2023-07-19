# Generated by Django 4.2.1 on 2023-06-21 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('author', '0006_author_hidden_author_hidden_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiaryPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('slug', models.CharField(blank=True, max_length=400, unique=True)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True, unique=True)),
                ('diary_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='diary_user', to='author.author')),
            ],
        ),
    ]
