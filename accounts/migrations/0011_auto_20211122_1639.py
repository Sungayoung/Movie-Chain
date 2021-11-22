# Generated by Django 3.2.6 on 2021-11-22 07:39

import accounts.models
from django.db import migrations, models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_user_nickname'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatting',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_img',
            field=imagekit.models.fields.ProcessedImageField(default='images/profile/default.jpg', storage=accounts.models.OverwriteStorage(), upload_to=accounts.models.profile_image_path),
        ),
    ]
