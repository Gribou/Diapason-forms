# Generated by Django 3.2.13 on 2022-10-20 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shared', '0010_safetycuberef'),
        ('similitude', '0005_auto_20221004_0810'),
    ]

    operations = [
        migrations.AddField(
            model_name='simi',
            name='safetycube',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_similitude', to='shared.safetycuberef', verbose_name='Référence SafetyCube'),
        ),
    ]
