# Generated by Django 3.2.12 on 2022-02-18 17:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('custom', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customform',
            name='enabled',
        ),
        migrations.CreateModel(
            name='FormCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=250, verbose_name='Intitulé')),
                ('rank', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
                ('show_in_toolbar', models.BooleanField(default=False, verbose_name="Afficher dans la barre d'outils")),
                ('include_fne', models.BooleanField(default=False, verbose_name='Inclure les FNE')),
                ('include_simi', models.BooleanField(default=False, verbose_name="Inclure les Similitudes d'Indicatifs")),
                ('include_brouillage', models.BooleanField(default=False, verbose_name='Inclure les Brouillages')),
                ('show_to_groups', models.ManyToManyField(blank=True, default=None, help_text="Si aucun groupe n'est sélectionné, cette catégorie sera visible par tous, y compris sans authentification", to='auth.Group', verbose_name='Montrer aux groupes')),
            ],
            options={
                'verbose_name': 'Catégorie',
                'verbose_name_plural': 'Catégories',
                'ordering': ['rank', 'label'],
            },
        ),
        migrations.AddField(
            model_name='customform',
            name='category',
            field=models.ForeignKey(blank=True, help_text="Le formulaire ne sera pas présenté aux utilisateurs si aucune catégorie n'est choisie", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forms', to='custom.formcategory', verbose_name='Catégorie'),
        ),
    ]
