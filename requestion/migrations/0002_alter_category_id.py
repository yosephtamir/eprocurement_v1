# Generated by Django 4.2.9 on 2024-05-16 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requestion', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
