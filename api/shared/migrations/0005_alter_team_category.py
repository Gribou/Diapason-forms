# Generated by Django 3.2.7 on 2021-12-15 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0004_adds_form_permissions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='category',
            field=models.CharField(blank=True, default='', help_text='Est utilisé pour catégoriser les fiches. Par exemple, E/W pour les centres ayant des zones de qualification.', max_length=2, verbose_name='Catégorie'),
        ),
    ]
