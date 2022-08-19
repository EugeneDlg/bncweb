# Generated by Django 4.0.3 on 2022-08-15 13:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Privileges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_other', models.BooleanField(default=False)),
                ('modify_self', models.BooleanField(default=False)),
                ('modify_other', models.BooleanField(default=False)),
                ('delete_self', models.BooleanField(default=False)),
                ('delete_other', models.BooleanField(default=False)),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, to_field='username')),
            ],
            options={
                'db_table': 'privileges',
                'ordering': ['id'],
            },
        ),
    ]
