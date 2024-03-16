# Generated by Django 5.0.3 on 2024-03-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_alter_chatsession_is_successful'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatsession',
            name='user_language',
            field=models.CharField(default='en', max_length=5),
        ),
        migrations.AlterField(
            model_name='leaderboard',
            name='language',
            field=models.CharField(default='en', max_length=5),
        ),
        migrations.AlterField(
            model_name='leaderboard',
            name='score',
            field=models.DecimalField(decimal_places=3, max_digits=7),
        ),
    ]
