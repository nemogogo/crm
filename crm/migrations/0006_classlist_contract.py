# Generated by Django 2.0.1 on 2018-02-08 05:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_contracttemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='classlist',
            name='contract',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.ContractTemplate'),
        ),
    ]