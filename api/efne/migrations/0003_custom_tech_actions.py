from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('efne', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Intitulé')),
                ('helperText', models.CharField(blank=True, max_length=250,
                 null=True, verbose_name="Message d'aide")),
            ],
            options={
                'verbose_name': 'Action technique',
                'verbose_name_plural': 'Actions techniques',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='fne',
            name='tech_actions_done',
            field=models.ManyToManyField(
                blank=True, default=None, to='efne.TechAction', verbose_name='Actions entreprises'),
        ),
        migrations.AddField(
            model_name='techeventtype',
            name='actions',
            field=models.ManyToManyField(
                blank=True, default=None, to='efne.TechAction', verbose_name='Actions à entreprendre'),
        ),
        migrations.RemoveField(
            model_name='fne',
            name='lvol',
        ),
        migrations.RemoveField(
            model_name='fne',
            name='odsarch',
        ),
        migrations.RemoveField(
            model_name='fne',
            name='vidage_str',
        ),
    ]
