# Generated by Django 3.1.3 on 2020-12-10 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201209_2000'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fieldanswer',
            name='field',
        ),
        migrations.AddField(
            model_name='fieldanswer',
            name='field',
            field=models.ManyToManyField(to='app.Field'),
        ),
        migrations.RemoveField(
            model_name='fieldanswer',
            name='user',
        ),
        migrations.AddField(
            model_name='fieldanswer',
            name='user',
            field=models.ManyToManyField(to='app.SimpleUser'),
        ),
        migrations.RemoveField(
            model_name='group',
            name='fields',
        ),
        migrations.AddField(
            model_name='group',
            name='fields',
            field=models.ManyToManyField(to='app.Field'),
        ),
    ]
