# Generated by Django 4.2.1 on 2025-04-04 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_periodico_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='periodico',
            name='logo',
            field=models.ImageField(max_length=200, upload_to='logos'),
        ),
    ]
