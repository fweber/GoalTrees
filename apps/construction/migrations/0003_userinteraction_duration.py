# Generated by Django 3.1.2 on 2021-05-25 11:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0002_read_prestudy_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinteraction',
            name='duration',
            field=models.IntegerField(null=True),
        ),
    ]
