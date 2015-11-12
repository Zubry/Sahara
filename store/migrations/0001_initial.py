# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contains',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('paid', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.ForeignKey(to='store.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField()),
                ('description', models.TextField(max_length=250)),
                ('stock_quantity', models.IntegerField()),
                ('price', models.BigIntegerField()),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Supplies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('product', models.ForeignKey(to='store.Product')),
                ('supplier', models.ForeignKey(to='store.Supplier')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=64)),
                ('salt', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=320)),
                ('is_staff', models.BooleanField()),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(to='store.User'),
        ),
        migrations.AddField(
            model_name='contains',
            name='order',
            field=models.ForeignKey(to='store.Order'),
        ),
        migrations.AddField(
            model_name='contains',
            name='product',
            field=models.ForeignKey(to='store.Product'),
        ),
    ]
