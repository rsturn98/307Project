# Generated by Django 3.0.4 on 2020-04-10 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_auto_20200401_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='player1Attack',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='player1Dodge',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='player2Attack',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='player2Dodge',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
