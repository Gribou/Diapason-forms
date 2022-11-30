# Generated by Django 3.2.12 on 2022-02-21 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('efne', '0005_alter_fnecounter_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fne',
            name='photo',
            field=models.FileField(blank=True, max_length=250, null=True, upload_to='fne/%Y/%m/photos/', verbose_name='Photo descriptive (DEPRECATED)'),
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(max_length=250, upload_to='fne/%Y/%m/attachments/', verbose_name='Pièce jointe')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='efne.fne')),
            ],
            options={
                'verbose_name': 'Pièce jointe',
                'verbose_name_plural': 'Pièces jointes',
            },
        ),
    ]