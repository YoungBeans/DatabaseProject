# Generated by Django 2.2.1 on 2019-06-01 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0003_auto_20190601_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='restid',
            field=models.AutoField(default=1, primary_key=True, serialize=False),
        ),
    ]