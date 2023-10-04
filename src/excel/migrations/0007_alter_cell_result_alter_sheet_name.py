# Generated by Django 4.2.5 on 2023-10-04 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0006_cell_result'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='result',
            field=models.CharField(blank=True),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='name',
            field=models.CharField(db_index=True, unique=True),
        ),
    ]
