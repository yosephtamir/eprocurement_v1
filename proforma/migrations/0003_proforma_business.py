# Generated by Django 4.2.9 on 2024-04-28 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('proforma', '0002_alter_proforma_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='proforma',
            name='business',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.businessinfo'),
        ),
    ]
