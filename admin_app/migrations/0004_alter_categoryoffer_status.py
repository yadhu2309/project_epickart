# Generated by Django 4.1 on 2022-09-24 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0003_categoryoffer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categoryoffer',
            name='status',
            field=models.BooleanField(max_length=20),
        ),
    ]
