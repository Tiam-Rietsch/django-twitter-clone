# Generated by Django 4.1.7 on 2023-03-13 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweet', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tweet',
            options={'ordering': ['-date_created']},
        ),
        migrations.AddField(
            model_name='tweet',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]