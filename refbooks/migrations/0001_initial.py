# Generated by Django 3.2.18 on 2023-03-12 12:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Refbook',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('code', models.CharField(max_length=100, unique=True, verbose_name='Код')),
                ('name', models.CharField(max_length=300, verbose_name='Наименование')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Справочник',
                'verbose_name_plural': 'Справочники',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('version', models.CharField(max_length=50, verbose_name='Версия')),
                ('date', models.DateField(verbose_name='Дата начала действия версии')),
                ('refbook', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='versions', to='refbooks.refbook', verbose_name='Наименование справочника')),
            ],
            options={
                'verbose_name': 'Версия справочника',
                'verbose_name_plural': 'Версии справочников',
                'ordering': ['-date'],
                'unique_together': {('refbook', 'date'), ('refbook', 'version')},
            },
        ),
        migrations.CreateModel(
            name='Element',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='Идентификатор')),
                ('code', models.CharField(max_length=100, verbose_name='Код элемента')),
                ('value', models.CharField(max_length=300, verbose_name='Значение элемента')),
                ('version', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='elements', to='refbooks.version', verbose_name='Версия')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
                'verbose_name_plural': 'Элементы справочников',
                'unique_together': {('version', 'code')},
            },
        ),
    ]