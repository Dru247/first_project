# Generated by Django 3.2.6 on 2022-09-26 18:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0034_auto_20220922_1117'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrandCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Название Марки')),
            ],
            options={
                'verbose_name': 'Марка ТС',
                'verbose_name_plural': 'Марки ТС',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ModelCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название Модели')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='modelcars', to='general_app.brandcar', verbose_name='Марка ТС')),
            ],
            options={
                'verbose_name': 'Модель ТС',
                'verbose_name_plural': 'Модели ТС',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='Дата')),
                ('location', models.CharField(max_length=200, verbose_name='Место')),
                ('state_number', models.CharField(max_length=20, verbose_name='Гос. номер')),
                ('payment', models.BooleanField(default=False, verbose_name='Оплата')),
                ('comment', models.CharField(max_length=200, verbose_name='Комментарий')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='installations', to='general_app.brandcar', verbose_name='Марка ТС')),
                ('human_worker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='installations', to='general_app.human', verbose_name='Установщик')),
                ('model', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='installations', to='general_app.modelcar', verbose_name='Модель ТС')),
                ('terminal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='installations', to='general_app.terminals', verbose_name='Терминал')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='installations', to='general_app.wialonuser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Установка',
                'verbose_name_plural': 'Установки',
                'ordering': ['-date'],
            },
        ),
    ]
