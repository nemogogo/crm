# Generated by Django 2.0.1 on 2018-04-12 05:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_courserecord_homework_title'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'permissions': (('audit_table_list', '可以查看audit每张表里所有的数据'), ('audit_table_list_view', '可以访问audit表里每条数据的修改页'), ('audit_table_list_change', '可以对audit表里的每条数据进行修改'), ('audit_table_obj_add_view', '可以访问audit每张表的数据增加页'), ('audit_table_obj_add', '可以对audit每张表进行数据添加'))},
        ),
    ]
