# Generated by Django 2.1 on 2018-07-17 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Info', '0003_phoneconfigurationoptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='phoneconfigurationoptions',
            name='Sip1_Enable',
            field=models.CharField(choices=[('Enabled', '启用'), ('Disabled', '禁用')], default='Disabled', max_length=32),
        ),
        migrations.AddField(
            model_name='phoneconfigurationoptions',
            name='Sip2_Enable',
            field=models.CharField(choices=[('Enabled', '启用'), ('Disabled', '禁用')], default='Disabled', max_length=32),
        ),
        migrations.AlterField(
            model_name='phoneconfigurationoptions',
            name='Sip1_UseOutboundProxy',
            field=models.CharField(choices=[('Enabled', '启用'), ('Disabled', '禁用')], default='Disabled', max_length=32),
        ),
        migrations.AlterField(
            model_name='phoneconfigurationoptions',
            name='Sip2_UseOutboundProxy',
            field=models.CharField(choices=[('Enabled', '启用'), ('Disabled', '禁用')], default='Disabled', max_length=32),
        ),
    ]
