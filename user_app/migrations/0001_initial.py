# Generated by Django 4.1 on 2022-09-24 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('admin_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=50)),
                ('address_line_1', models.CharField(max_length=50)),
                ('address_line_2', models.CharField(blank=True, max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('zip_code', models.IntegerField(null=True)),
                ('order_total', models.FloatField()),
                ('status', models.CharField(choices=[('New', 'New'), ('Confirmed', 'Confirmed'), ('Shipped', 'Shipped'), ('Out of delivery', 'Out of delivery'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Confirmed', max_length=50)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserSignUp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=50)),
                ('psw', models.CharField(max_length=50)),
                ('psw1', models.CharField(max_length=50)),
                ('status', models.BooleanField(max_length=20)),
                ('logstatus', models.BooleanField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.product')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.usersignup')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('payment_method', models.CharField(max_length=100)),
                ('amount_paid', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.usersignup')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('product_price', models.FloatField()),
                ('ordered', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('New', 'New'), ('Confirmed', 'Confirmed'), ('Shipped', 'Shipped'), ('Out of delivery', 'Out of delivery'), ('Cancelled', 'Cancelled'), ('Returned', 'Returned')], default='Confirmed', max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.order')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_app.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.usersignup')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_app.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_app.usersignup'),
        ),
        migrations.CreateModel(
            name='Cart_view',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.IntegerField()),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tot_amt', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_app.product')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.usersignup')),
            ],
        ),
        migrations.CreateModel(
            name='Cart_total',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amt', models.DecimalField(decimal_places=2, max_digits=8)),
                ('cid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.cart_view')),
                ('uid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_app.usersignup')),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('address_line_1', models.CharField(max_length=100)),
                ('address_line_2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip', models.IntegerField()),
                ('phone', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=100)),
                ('user', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='user_app.usersignup')),
            ],
        ),
    ]
