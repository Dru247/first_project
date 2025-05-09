# Generated by Django 3.2.6 on 2021-09-08 15:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general_app', '0010_wialonobject_wialonuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='WialonObjectActive',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('wialon_object', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='general_app.wialonobject')),
            ],
        ),
    ]
