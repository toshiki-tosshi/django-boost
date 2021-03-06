# Generated by Django 2.1.5 on 2019-04-26 06:23

from django.db import migrations, models
import django_boost.models.fields
import django_boost.models.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('registered_at', models.DateField(auto_now_add=True)),
                ('color', django_boost.models.fields.ColorCodeFiled(max_length=7)),
            ],
            bases=(django_boost.models.mixins.JsonMixin, models.Model),
        ),
    ]
