# Generated by Django 4.2.5 on 2023-10-02 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('excel', '0003_cell_name_alter_cell_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cell',
            name='name',
            field=models.CharField(db_index=True),
        ),
        migrations.AlterField(
            model_name='cell',
            name='value',
            field=models.CharField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sheet',
            name='name',
            field=models.CharField(db_index=True, default='DELETE_ME'),
            preserve_default=False,
        ),
    ]
