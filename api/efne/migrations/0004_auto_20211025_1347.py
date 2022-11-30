# Generated by Django 3.2.7 on 2021-10-25 13:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0002_userdetail_be_notified_on_simi'),
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('efne', '0003_custom_tech_actions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fne',
            options={'ordering': ['event_date'], 'verbose_name': 'Formulaire', 'verbose_name_plural': 'Formulaires'},
        ),
        migrations.AlterModelOptions(
            name='fnecounter',
            options={'verbose_name': 'Compteur', 'verbose_name_plural': 'Statistiques'},
        ),
        migrations.AddField(
            model_name='subdata',
            name='alarm_acknowledged',
            field=models.BooleanField(default=False, verbose_name='Rappel acquitté'),
        ),
        migrations.AddField(
            model_name='subdata',
            name='is_safety_event',
            field=models.BooleanField(default=False, verbose_name='Evènement sécurité'),
        ),
        migrations.AlterField(
            model_name='fneaction',
            name='current_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='efne_graph_for_current_group', to='auth.group', verbose_name='Responsable actuel'),
        ),
        migrations.AlterField(
            model_name='fneaction',
            name='current_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='efne_graph_for_current', to='shared.status', verbose_name='Statut actuel'),
        ),
        migrations.AlterField(
            model_name='fneaction',
            name='next_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='efne_graph_for_next_group', to='auth.group', verbose_name='Prochain responsable'),
        ),
        migrations.AlterField(
            model_name='fneaction',
            name='next_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='efne_graph_for_next', to='shared.status', verbose_name='Prochain statut'),
        ),
        migrations.AlterField(
            model_name='fnecounter',
            name='id_list_as_string',
            field=models.TextField(help_text='Liste des identifiants uniques de fiche séparées par des points-virgules', verbose_name='Liste des fiches'),
        ),
        migrations.AlterField(
            model_name='postit',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='efne_postits', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='redactor',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='efne_redactors', to='shared.team'),
        ),
    ]