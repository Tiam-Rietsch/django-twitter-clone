# Generated by Django 4.1.7 on 2023-03-26 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('replies', '0006_alter_reply_attachement'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='attachement',
            field=models.ImageField(blank=True, null=True, upload_to='attachements/'),
        ),
    ]
