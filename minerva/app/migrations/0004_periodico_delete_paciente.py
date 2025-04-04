# Generated by Django 4.2.1 on 2025-04-04 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_paciente'),
    ]

    operations = [
        migrations.CreateModel(
            name='Periodico',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('url', models.URLField()),
                ('logo', models.ImageField(height_field=256, max_length=200, upload_to='media/logos', width_field=256)),
            ],
        ),
        migrations.DeleteModel(
            name='paciente',
        ),
    ]
