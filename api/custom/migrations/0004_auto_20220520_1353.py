# Generated by Django 3.2.12 on 2022-05-20 13:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom', '0003_auto_20220219_0916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customfield',
            name='choices',
            field=models.ForeignKey(blank=True, help_text="Pour les champs de type 'Liste de sélection', 'Boutons radio', 'Groupe de cases à cocher', 'Groupes de boutons'", null=True, on_delete=django.db.models.deletion.SET_NULL, to='custom.selectionlist', verbose_name='Liste de choix'),
        ),
        migrations.AlterField(
            model_name='customfield',
            name='type',
            field=models.CharField(choices=[('text-input', 'Champ Texte'), ('password', 'Champ Mot de passe'), ('checkbox', 'Case à cocher'), ('checkbox-group', 'Groupe de cases à cocher'), ('radio', 'Boutons radio'), ('button', 'Bouton seul'), ('button-group', 'Groupe de boutons'), ('select', 'Liste de sélection'), ('date', 'Champ Date'), ('time', 'Champ Heure'), ('datetime', 'Champ Date et Heure'), ('photo', 'Photo'), ('drawing', 'Schéma'), ('text', 'Texte explicatif'), ('divider', 'Séparateur'), ('empty', 'Vide')], default='text-input', max_length=100, verbose_name='Type de champ'),
        ),
    ]
