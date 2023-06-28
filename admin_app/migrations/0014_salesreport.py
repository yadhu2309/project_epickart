# Generated by Django 4.1 on 2022-09-28 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0013_productoffer'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productName', models.CharField(max_length=100)),
                ('categoryName', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('quantity', models.IntegerField()),
                ('productPrice', models.FloatField()),
            ],
        ),
    ]