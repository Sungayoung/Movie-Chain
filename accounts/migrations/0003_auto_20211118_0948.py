# Generated by Django 3.2.6 on 2021-11-18 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
