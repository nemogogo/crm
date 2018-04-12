# Generated by Django 2.0.1 on 2018-02-09 13:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0006_classlist_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='stu_account',
            field=models.ForeignKey(blank=True, help_text='只有学员报名后方可为其创建账号', null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.Customer', verbose_name='关联学员账号'),
        ),
        migrations.AlterField(
            model_name='customer',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '未报名'), (1, '已报名')]),
        ),
    ]
