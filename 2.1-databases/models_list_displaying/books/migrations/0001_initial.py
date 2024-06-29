# Generated by Django 4.2.13 on 2024-06-28 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
                ('author', models.CharField(max_length=64, verbose_name='Автор')),
                ('pub_date', models.DateField(verbose_name='Дата публикации')),
            ],
        ),
    ]
