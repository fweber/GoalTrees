# Generated by Django 3.1.2 on 2021-09-13 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0015_auto_20210907_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='goal',
            name='replicated_tree_id',
            field=models.IntegerField(null=True),
        ),
    ]
