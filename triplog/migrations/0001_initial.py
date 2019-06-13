# Generated by Django 2.2.1 on 2019-05-22 06:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=255)),
                ('category_status', models.CharField(choices=[('0', 'Unpublished'), ('1', 'Published')], default='1', max_length=1)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=255)),
                ('location_body', models.TextField(blank=True)),
                ('location_status', models.CharField(choices=[('0', 'Unpublished'), ('1', 'Published')], default='1', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trip_name', models.CharField(max_length=255)),
                ('trip_body', models.TextField()),
                ('trip_status', models.CharField(choices=[('0', 'Unpublished'), ('1', 'Published')], default='1', max_length=1)),
                ('trip_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='triplog.Category')),
                ('trip_location', models.ManyToManyField(to='triplog.Location')),
                ('trip_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]