# Generated by Django 3.2.6 on 2021-11-19 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charactername',
            name='character',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
