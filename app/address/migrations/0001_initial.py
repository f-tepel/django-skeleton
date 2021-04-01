# Generated by Django 3.1.6 on 2021-02-15 20:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
            ],
        ),
    ]