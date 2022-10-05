# Generated by Django 4.1 on 2022-09-25 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_app', '0009_frontbanner_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='BannerApplied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False, max_length=20)),
                ('banner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.frontbanner')),
            ],
        ),
    ]
