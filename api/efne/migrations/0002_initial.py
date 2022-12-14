# Generated by Django 3.2.7 on 2021-10-23 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('efne', '0001_initial'),
        ('shared', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='redactor',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='redactors', to='shared.team'),
        ),
        migrations.AddField(
            model_name='postit',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='postit',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postits', to='efne.subdata'),
        ),
        migrations.AddField(
            model_name='fneaction',
            name='current_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='graph_for_current_group', to='auth.group', verbose_name='Responsable actuel'),
        ),
        migrations.AddField(
            model_name='fneaction',
            name='current_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='graph_for_current', to='shared.status', verbose_name='Statut actuel'),
        ),
        migrations.AddField(
            model_name='fneaction',
            name='next_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='graph_for_next_group', to='auth.group', verbose_name='Prochain responsable'),
        ),
        migrations.AddField(
            model_name='fneaction',
            name='next_status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='graph_for_next', to='shared.status', verbose_name='Prochain statut'),
        ),
        migrations.AddField(
            model_name='fne',
            name='assigned_to_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='efne', to='auth.group', verbose_name='Attribu?? ??'),
        ),
        migrations.AddField(
            model_name='fne',
            name='available_actions',
            field=models.ManyToManyField(blank=True, default=None, editable=False, to='efne.FneAction', verbose_name='Actions possibles'),
        ),
        migrations.AddField(
            model_name='fne',
            name='event_types',
            field=models.ManyToManyField(blank=True, default=None, to='efne.EventType', verbose_name="Types d'??v??nements"),
        ),
        migrations.AddField(
            model_name='fne',
            name='status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='efne', to='shared.status', verbose_name='Statut'),
        ),
        migrations.AddField(
            model_name='fne',
            name='tech_event',
            field=models.ManyToManyField(blank=True, default=None, to='efne.TechEventType', verbose_name="Types d'??v??nements techniques"),
        ),
        migrations.AddField(
            model_name='cdsreport',
            name='parent_fne',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='cds_report', to='efne.fne', verbose_name='FNE parente'),
        ),
        migrations.AddField(
            model_name='aircraft',
            name='fne',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircrafts', to='efne.fne'),
        ),
    ]
