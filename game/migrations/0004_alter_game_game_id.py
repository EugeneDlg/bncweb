# Generated by Django 4.0.3 on 2022-05-11 20:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_remove_game_finish_time_remove_game_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='game_id',
            field=models.CharField(max_length=251, unique=True),
        ),
    ]