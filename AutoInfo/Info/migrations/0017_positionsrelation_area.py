# Generated by Django 2.1 on 2018-12-21 02:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Info', '0016_auto_20180728_0902'),
    ]

    operations = [
        migrations.AddField(
            model_name='positionsrelation',
            name='area',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]