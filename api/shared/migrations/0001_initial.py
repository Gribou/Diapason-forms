# Generated by Django 3.2.7 on 2021-10-23 05:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=10, unique=True, verbose_name='Intitulé')),
            ],
            options={
                'verbose_name': 'Position de contrôle',
                'verbose_name_plural': 'Positions de contrôle',
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=10, unique=True, verbose_name='Intitulé')),
            ],
            options={
                'verbose_name': 'Secteur',
                'verbose_name_plural': 'Secteurs',
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='SectorGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=10, unique=True, verbose_name='Intitulé')),
            ],
            options={
                'verbose_name': 'Regroupement',
                'verbose_name_plural': 'Regroupements',
                'ordering': ('label',),
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25, verbose_name='Intitulé')),
                ('is_draft', models.BooleanField(default=False)),
                ('is_waiting', models.BooleanField(default=False)),
                ('is_in_progress', models.BooleanField(default=False)),
                ('is_done', models.BooleanField(default=False)),
                ('is_to_be_deleted', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Statut',
                'verbose_name_plural': 'Statuts',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=10, unique=True, verbose_name='Intitulé')),
                ('category', models.CharField(max_length=2, verbose_name='Catégorie')),
                ('rank', models.PositiveIntegerField(default=0, verbose_name='Ordre')),
            ],
            options={
                'verbose_name': 'Equipe',
                'verbose_name_plural': 'Equipes',
                'ordering': ('rank',),
            },
        ),
        migrations.CreateModel(
            name='UserDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('be_notified_on_fne', models.BooleanField(default=False, verbose_name='Notification FNE')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GroupDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_validator', models.BooleanField(default=False, verbose_name='Validateur')),
                ('is_investigator', models.BooleanField(default=False, verbose_name='Investigateur')),
                ('has_all_access', models.BooleanField(default=False, verbose_name='Accès complet')),
                ('group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='auth.group')),
            ],
        ),
    ]
