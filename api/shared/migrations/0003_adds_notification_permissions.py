# Generated by Django 3.2.7 on 2021-11-05 08:45

from django.db import migrations

# permissions are created during post_migrate


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0002_userdetail_be_notified_on_simi'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdetail',
            options={'permissions': (('be_notified_on_fne', 'Etre notifié pour les FNE'), (
                'be_notified_on_simi', 'Etre notifié pour les fiches similitudes'))},
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='be_notified_on_fne',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='be_notified_on_simi',
        ),
        migrations.RemoveField(
            model_name='userdetail',
            name='user',
        ),
    ]
