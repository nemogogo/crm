# Generated by Django 2.0.1 on 2018-02-06 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='role',
            field=models.ManyToManyField(blank=True, null=True, to='crm.Role'),
        ),
    ]