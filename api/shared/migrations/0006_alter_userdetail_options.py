# Generated by Django 3.2.7 on 2021-12-15 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0005_alter_team_category'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userdetail',
            options={'permissions': (('be_notified_on_fne', 'Etre notifié pour les FNE'), ('be_notified_on_simi', 'Etre notifié pour les fiches similitudes'), ('be_notified_on_brouillage', 'Etre notifié pour les fiches brouillage'))},
        ),
    ]
