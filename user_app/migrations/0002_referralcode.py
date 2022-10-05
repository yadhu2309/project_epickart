# Generated by Django 4.1 on 2022-09-24 16:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReferralCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('refer_code', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=True, max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.usersignup')),
            ],
        ),
    ]
