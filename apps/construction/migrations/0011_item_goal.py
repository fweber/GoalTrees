# Generated by Django 3.1.2 on 2021-07-19 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('construction', '0010_item_personal_goal'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='goal',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='construction.goal'),
        ),
    ]
