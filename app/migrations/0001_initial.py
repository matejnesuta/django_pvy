# Generated by Django 3.0.5 on 2020-04-28 13:08

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('last_update', models.DateTimeField(auto_now=True)),
                ('file', models.CharField(max_length=200, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Interpret',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazev', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['nazev'],
            },
        ),
        migrations.CreateModel(
            name='Zanr',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Zakaznik',
            fields=[
                ('email', models.EmailField(max_length=254, primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('country', models.ForeignKey(blank=True, on_delete=models.SET(''), to='app.Country')),
            ],
            options={
                'ordering': ['last_name', 'first_name', 'country'],
            },
        ),
        migrations.CreateModel(
            name='Vydavatelstvi',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazev', models.CharField(max_length=200, unique=True)),
                ('vznik', models.IntegerField(validators=[django.core.validators.MinValueValidator(1800), django.core.validators.MaxValueValidator(2020)])),
                ('vlastnik', models.CharField(blank=True, max_length=100)),
                ('sidlo', models.ForeignKey(blank=True, on_delete=models.SET(''), to='app.Country')),
            ],
            options={
                'ordering': ['nazev', 'vznik'],
            },
        ),
        migrations.CreateModel(
            name='Polozka',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazev', models.CharField(max_length=100)),
                ('stopaz', models.TimeField()),
                ('rok_vydani', models.IntegerField(validators=[django.core.validators.MinValueValidator(1000), django.core.validators.MaxValueValidator(2020)])),
                ('typ', models.CharField(blank=True, choices=[('ep', 'EP'), ('lp', 'LP'), ('kompilace', 'Kompilace'), ('soundtrack', 'Soundtrack'), ('singl', 'Singl'), ('remix ep', 'Remix EP')], max_length=10)),
                ('explicitnost', models.CharField(choices=[('ano', 'Ano'), ('ne', 'Ne')], max_length=3)),
                ('cena', models.FloatField(validators=[django.core.validators.MinValueValidator(0)])),
                ('cover', models.ManyToManyField(to='app.Cover')),
                ('interpret', models.ManyToManyField(to='app.Interpret')),
                ('vydavatelstvi', models.ManyToManyField(blank=True, to='app.Vydavatelstvi')),
                ('zanr', models.ManyToManyField(to='app.Zanr')),
            ],
            options={
                'ordering': ['interpret__nazev', '-rok_vydani'],
            },
        ),
        migrations.CreateModel(
            name='Objednavka',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nazev', models.ManyToManyField(to='app.Polozka')),
                ('zakaznik', models.ManyToManyField(to='app.Zakaznik')),
            ],
            options={
                'ordering': ['zakaznik__email'],
            },
        ),
    ]