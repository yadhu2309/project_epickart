# Generated by Django 4.1 on 2022-09-28 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0005_returnedorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='created_at',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orderproduct',
            name='updated_at',
            field=models.DateField(auto_now=True),
        ),
    ]
